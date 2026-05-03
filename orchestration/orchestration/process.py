"""
Process telemetry Parquet files into a clean, time-ordered dataset.

This stage transforms raw flight telemetry into a structured format suitable for
feature engineering and analysis.

Key steps:
- Normalize column names
- Construct a unified timestamp from date/time components
- Sort records chronologically

Input:
- data/raw/parquet/

Output:
- data/processed/parquet/

Design principles:
- Lightweight transformation (no heavy cleaning)
- Preserve raw signal behavior for downstream analysis
"""

import io
import pandas as pd
from dagster import asset, MaterializeResult
from .ingest import ingest_raw_csv_to_parquet
from .s3_utils import (get_file_list, has_been_processed, is_file,
                       upload_to_s3, get_s3_file)

from .config import (
    DATE_COLS,
    S3_PROCESSED_PATH,
    S3_PARQUET_PATH,
    S3_BUCKET
)

def load_flight(key):
    return pd.read_parquet(get_s3_file(S3_BUCKET, key))

def build_timestamp(df):
    for col in DATE_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["timestamp"] = pd.to_datetime({
        "year": df["DATE_YEAR"],
        "month": df["DATE_MONTH"],
        "day": df["DATE_DAY"],
        "hour": df["GMT_HOUR"],
        "minute": df["GMT_MINUTE"],
        "second": df["GMT_SEC"],
    }, errors="coerce")
    return df

def normalize_data(df):
    df.columns = df.columns.str.strip()
    return df

def sort_and_clean(df):
    df = df.sort_values(by=["timestamp"]).reset_index(drop=True)
    return df

@asset(deps=[ingest_raw_csv_to_parquet])
def process():
    print("Starting process...")

    processed = 0
    skipped = 0
    failed = 0

    s3_parquet_files = get_file_list(S3_BUCKET, S3_PARQUET_PATH)

    for parquet_file_name in s3_parquet_files:
        key = parquet_file_name["Key"]

        # Build Parquet processed output path
        processed_file_name = key.replace(S3_PARQUET_PATH, S3_PROCESSED_PATH)

        # Don't process if it isn't a file
        if not is_file(processed_file_name, file_ext='.parquet'):
            continue

        try:
            print(f"Processing {processed_file_name}")
            
            # Checking to usee if file has been processed
            if has_been_processed(S3_BUCKET, processed_file_name):
                print(f"Skipping: {processed_file_name}")
                skipped += 1
                continue

            df = load_flight(key)
            df = normalize_data(df)
            df = build_timestamp(df)
            df = sort_and_clean(df)

            # puts parquet in buffer
            buffer = io.BytesIO()
            df.to_parquet(buffer, engine="pyarrow", index=False)
            buffer.seek(0)

            upload_to_s3(S3_BUCKET, processed_file_name, buffer)
            processed += 1

        except Exception as e:
            failed += 1
            print(f"Exception while processing {processed_file_name}: {e}")

    # Outputs summary counts of processed and failed files
    print("SUMMARY RESULTS")
    print(f"Processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")

    return MaterializeResult(
        metadata = {
            "processed": processed,
            "skipped": skipped,
            "failed": failed
        }
    )
