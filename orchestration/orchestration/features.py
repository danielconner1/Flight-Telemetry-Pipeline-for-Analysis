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
from dagster import asset, MaterializeResult
from .ingest import ingest_raw_csv_to_parquet
from .process import process

from .config import (
    PROCESSED_PARQUET_DATA_PATH,
    FEATURES_OUTPUT_PATH
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

    status = "Success"
    for file in PROCESSED_PARQUET_DATA_PATH.glob("*.parquet"):
        try:
            print(f"Processing {file.name}")
            df = pd.read_parquet(file)

            summary = build_summary_features(df, file.name)
            summaries.append(summary)

        except Exception as e:
            print(f"Failed: {file.name} -> {e}")
            status = "Failed"

    summary_df = pd.DataFrame(summaries)

    FEATURES_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_parquet(FEATURES_OUTPUT_PATH, index=False)

    print("\nSummary dataset created")
    print(summary_df.head())

    return MaterializeResult(
        metadata= {
            "status":status
        }
    )
