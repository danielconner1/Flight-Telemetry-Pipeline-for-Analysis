# Flight Telemetry Data Pipeline

This project is a telemetry data pipeline built with Python, Dagster, Docker, AWS, and PostgreSQL.

The pipeline ingests raw aviation telemetry CSV files, converts them to Parquet, processes and standardizes the data, and generates summary flight features for analytics and future machine learning use cases.

The system is orchestrated with Dagster and deployed using Dagster+ Hybrid on AWS EC2.

## What the Pipeline Does

### Ingest
- Reads raw telemetry CSV files
- Converts files to Parquet
- Skips files that were already processed

### Process
- Cleans and standardizes telemetry data
- Builds timestamps
- Sorts records chronologically
- Removes invalid records

### Feature Engineering
Creates one summary row per flight with metrics such as:
- Flight duration
- Maximum altitude
- Average airspeed
- Ground speed statistics
- Altitude variability
- Climb and descent metrics

Summary features and pipeline run metadata are loaded into PostgreSQL.

## Tech Stack

- Python
- Pandas
- Dagster
- PostgreSQL
- Docker
- AWS S3
- AWS EC2
- AWS ECR
- GitHub Actions

## Deployment

The pipeline is deployed using Dagster+ Hybrid on AWS EC2.

GitHub Actions:
- builds the Docker image
- pushes the image to AWS ECR
- deploys updates to Dagster Cloud

## Current Capabilities

- End-to-end telemetry ingestion pipeline
- Asset orchestration with Dagster
- S3-based ingestion workflow
- Dockerized execution
- CI/CD deployment pipeline
- PostgreSQL integration
- Cloud deployment using Dagster+ Hybrid

## Future Improvements

- Data quality validation
- Observability dashboards in Grafana
- Anomaly detection models
- Additional telemetry features
