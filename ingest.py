"""
Convert raw telemetry CSV files to Parquet format with minimal preprocessing.
Skips existing files and logs processing results.

"""

import pandas as pd
from pathlib import Path
import boto3

RAW_CSV_DATA_PATH = Path("data/raw/csv/")
RAW_PARQUET_DATA_PATH = Path("data/raw/parquet/")
DATE_COLS = ["DATE_YEAR", "DATE_MONTH", "DATE_DAY", "GMT_HOUR", "GMT_MINUTE", "GMT_SEC"]
BUCKET = 'telemetrypipeline'
RAW_PATH = 'raw/incoming/'
PROCESSED_PATH = 'raw/processed/'

def get_raw_incoming_files():
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket='s3://telemetrypipeline/raw/incoming')
    return set(response['Body'])

def main():
    print("Starting ingest...")

    processed = 0
    skipped = 0
    failed = 0

    if not RAW_CSV_DATA_PATH.exists():
        raise FileNotFoundError(
            f"{RAW_CSV_DATA_PATH} does not exist. "
            "Download data from Kaggle: "
            "https://www.kaggle.com/datasets/gijsbekkers/qar-flight-data?resource=download "
            f"and place data in {RAW_CSV_DATA_PATH}"
        )

    # Creates parquet data path if doesn't exist. If it exists, we do nothing.
    RAW_PARQUET_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    for csv_file_name in RAW_CSV_DATA_PATH.glob("*.csv"):

        print(f"Processing {csv_file_name.name}")

        try:
            df = pd.read_csv(csv_file_name)
        except Exception as e:
            print(f"Exception while reading {csv_file_name.name}: {e}")
            continue

        # Build Parquet output path from CSV filename
        parquet_file_name = RAW_PARQUET_DATA_PATH / csv_file_name.with_suffix(".parquet").name

        # Cast date/time fields to smaller integer types (int16) since values are small,
        # reducing memory footprint without losing precision
        for col in DATE_COLS:
            df[col] = df[col].astype("int16")

        # Convert unprocessed CSV files to Parquet
        if parquet_file_name.exists():
            print(f"Skipping: {parquet_file_name.name}")
            skipped += 1
        else:
            try:
                df.to_parquet(parquet_file_name,engine="pyarrow", index=False)
                processed += 1
                print(f"Saved: {parquet_file_name.name}")

            except Exception as e:
                failed += 1
                print(f"Failed to write parquet file: {parquet_file_name}", e)

    # Outputs summary counts of processed and failed files
    print("SUMMARY RESULTS")
    print(f"Processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    main()





