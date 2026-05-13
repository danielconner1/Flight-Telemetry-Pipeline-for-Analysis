from dagster import define_asset_job, ScheduleDefinition, Definitions

telemetry_job = define_asset_job(
    name="telemetry_job",
    selection=[
        "ingest_raw_csv_to_parquet",
        "process",
        "features",
    ],
)

telemetry_schedule = ScheduleDefinition(
    name="telemetry_daily",
    job=telemetry_job,
    cron_schedule="0 8 * * *",
)
