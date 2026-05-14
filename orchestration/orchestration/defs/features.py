"""
Generate flight-level summary features from processed telemetry data.

This stage aggregates time-series flight data into a single row per flight,
capturing both overall state and dynamic behavior. These features are designed
to support anomaly detection and downstream modeling.

Key features:
- Flight duration
- Altitude statistics (max, mean, standard deviation, range)
- Airspeed statistics (true and ground speed mean and variability)
- Dynamic behavior metrics (climb rate, speed change, variability)

Input:
- data/processed/parquet/

Output:
- data/features/flight_summary.parquet

Design principles:
- One row per flight for model-ready dataset
- Combine static and dynamic feature representations
"""

import pandas as pd
import os
from datetime import datetime, timezone
from dagster import asset, MaterializeResult
from .ingest import ingest_raw_csv_to_parquet
from .process import process
import io
from ..s3_utils import (get_file_list,
                       is_file, upload_to_s3, get_df_from_s3_parquet)
from ..db_utils import insert_into_pipeline_runs_table, get_pipeline_runs_count

from ..config import (
    S3_PROCESSED_PATH,
    S3_BUCKET,
    S3_FEATURES_FILE_NAME,
    S3_FEATURES_PATH
)

def build_summary_features(df: pd.DataFrame, file_name: str) -> dict:

    print("Building summary features..")

    return {
        "file_name": file_name,
        "flight_duration": (df["timestamp"].max() - df["timestamp"].min()).total_seconds(),
        "max_altitude": df["ALT"].max(),
        "mean_altitude": df["ALT"].mean(),
        "altitude_std": df["ALT"].std(),
        "true_airspeed_mean": df["TAS"].mean(),
        "true_airspeed_std": df["TAS"].std(),
        "ground_speed_mean": df["GS"].mean(),
        "ground_speed_std": df["GS"].std(),
        "altitude_range": df["ALT"].max() - df["ALT"].min(),
        "true_airspeed_range": df["TAS"].max() - df["TAS"].min(),

    }

@asset(deps=[ingest_raw_csv_to_parquet,process])
def features():
    summaries = []

    started = datetime.now(timezone.utc)
    status = "Success"
    s3_processed_files = get_file_list(S3_BUCKET, S3_PROCESSED_PATH)

    for processed_file in s3_processed_files:
        try:
            processed_file_name = processed_file["Key"]

            # Don't process if it isn't a file
            if not is_file(processed_file_name, file_ext='.parquet'):
                continue

            print(f"Processing {processed_file_name}")
            df = get_df_from_s3_parquet(S3_BUCKET, processed_file_name)

            summary = build_summary_features(df, processed_file_name)
            summaries.append(summary)

        except Exception as e:
            print(f"Failed: {processed_file_name} -> {e}")
            status = "Failed"

    summary_df = pd.DataFrame(summaries)

    # puts parquet in buffer
    buffer = io.BytesIO()
    summary_df.to_parquet(buffer, engine="pyarrow", index=False)
    buffer.seek(0)

    upload_to_s3(S3_BUCKET, S3_FEATURES_FILE_NAME, buffer)

    print("\nSummary dataset created")
    print(summary_df.head())

    ended = datetime.now(timezone.utc)

    total_file_num = len(s3_processed_files)

    conn_str = os.environ.get("POSTGRES_URL")

    if not conn_str:
        print("Postgres URL not configured")

    table_count = get_pipeline_runs_count(conn_str)

    print("Pipeline runs count before insert:", table_count)
    print("Inserting into pipeline_runs table...")

    insert_into_pipeline_runs_table(started, ended, total_file_num, 0, 0,
                                    "features", conn_str)

    table_count = get_pipeline_runs_count(conn_str)

    print("Pipeline runs count after insert:", table_count)

    return MaterializeResult(
        metadata= {
            "status":status
        }
    )
