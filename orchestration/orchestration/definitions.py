from dagster import Definitions

from .ingest import ingest_raw_csv_to_parquet
from .process import process

defs = Definitions(
    assets=[
        ingest_raw_csv_to_parquet,
        process
    ],
)