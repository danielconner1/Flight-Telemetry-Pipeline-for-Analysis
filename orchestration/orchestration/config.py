from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_CSV_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "csv"
RAW_PARQUET_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "parquet"
DATE_COLS = ["DATE_YEAR", "DATE_MONTH", "DATE_DAY", "GMT_HOUR", "GMT_MINUTE", "GMT_SEC"]
PROCESSED_PARQUET_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "parquet"
FEATURES_OUTPUT_PATH = PROJECT_ROOT / "data" / "features" / "flight_summary.parquet"
