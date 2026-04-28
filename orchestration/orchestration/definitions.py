from dagster import Definitions, define_asset_job, ScheduleDefinition

from .ingest import ingest_raw_csv_to_parquet
from .process import process
from .features import features

telemetry_schedule = ScheduleDefinition(
    name="telemetry_daily",
    job=telemetry_job,
    cron_schedule="0 8 * * *",  # every day at 8am (for testing)
)

telemetry_job = define_asset_job(
    name="telemetry_pipeline_job",
    selection=[
        "ingest_raw_csv_to_parquet",
        "process",
        "features",
    ],

)

defs = Definitions(
    assets=[
        ingest_raw_csv_to_parquet,
        process,
        features
    ],
    jobs=[telemetry_job],
)