# Flight Telemetry Data Pipeline

This project implements an end-to-end, production-style data engineering pipeline for aviation telemetry data using Python, Dagster, Docker, and AWS. It ingests raw flight telemetry, standardizes time-series signals, and produces a structured, model-ready dataset. The system is orchestrated using Dagster and deployed using a hybrid cloud architecture with Dagster+ and AWS EC2. In addition to pipeline development, this project demonstrates real-world operational concerns including orchestration, CI/CD, containerization, cloud deployment, and infrastructure reliability.

## Overview

Telemetry data presents several real-world challenges:

- Sensors operate at different sampling rates  
- Continuous signals (altitude, speed) are mixed with discrete state changes  
- Data is often incomplete or noisy  
- Raw data is not directly usable for analytics or machine learning  

This pipeline transforms raw telemetry into consistent, structured, and feature-rich datasets suitable for downstream analytics.

## Pipeline Architecture

```
Raw CSV Files
      ↓
   Ingest
      ↓
Raw Parquet Files
      ↓
   Process
      ↓
Processed Parquet Files
      ↓
Feature Engineering
      ↓
Flight Summary Dataset
```

Each stage is implemented as a Dagster asset, enabling dependency tracking, selective execution, and observability.

## End-to-End System Architecture

```
GitHub
   ↓
GitHub Actions (CI/CD)
   ↓
Docker Build & Push
   ↓
AWS ECR (Container Images)
   ↓
EC2 Instance (t3.medium)
   ↓
┌─────────────────────────────────────────┐
│ Dagster Cloud Agent                    │
│   ├─ Code Server (gRPC)                │
│   ├─ Run Containers                    │
│   └─ Pipeline Execution Orchestration  │
└─────────────────────────────────────────┘
   ↓
Dagster+ UI (Monitoring & Execution)
```

## Pipeline Stages

### Ingest

- Reads raw CSV telemetry files  
- Converts files to Parquet format  
- Skips already processed files  
- Tracks ingestion metrics  

Output:

```
data/raw/parquet/
```

### Process

- Normalizes column names  
- Constructs unified timestamps  
- Sorts telemetry chronologically  
- Removes invalid or incomplete records  

Output:

```
data/processed/parquet/
```

### Feature Engineering

Aggregates time-series telemetry into one row per flight.

Features include:

- Flight duration  
- Maximum altitude  
- Mean altitude  
- Altitude standard deviation  
- Altitude range  
- True airspeed statistics  
- Ground speed statistics  
- Derived dynamic metrics (climb rate, variability)  

Output:

```
data/features/flight_summary.parquet
```

## Orchestration

The pipeline is orchestrated using Dagster’s asset-based model.

Capabilities include:

- Asset lineage tracking  
- Dependency management  
- Partial or full pipeline execution  
- Execution logs and metadata  
- Observability through Dagster UI  
- Job-based execution  

Pipeline entry point:

```
orchestration.orchestration.definitions
```

## Local Execution

```
cd orchestration
dagster dev -m orchestration.orchestration.definitions
```

Open:

```
http://localhost:3000
```

## Docker Execution

```
docker build -t telemetry-pipeline .
docker run --rm -p 3000:3000 telemetry-pipeline
```

## Cloud Deployment (Dagster+ Hybrid)

The pipeline is deployed using Dagster Cloud Hybrid on AWS EC2.

- Docker image built via CI/CD  
- Image pushed to AWS ECR  
- EC2 instance runs:  
  - Dagster Cloud Agent  
  - Code Server (gRPC)  
  - Run containers for execution  

This mirrors a production-style data engineering environment.

## CI/CD

CI/CD is implemented using GitHub Actions:

- Build Docker image  
- Push to AWS ECR  
- Deploy to Dagster Cloud  
- Update code location automatically  

This enables consistent, reproducible deployments.


## Current Capabilities

- End-to-end telemetry pipeline  
- Asset-based orchestration with Dagster  
- Dockerized execution  
- CI/CD deployment pipeline  
- Hybrid cloud orchestration (Dagster+)  
- Production debugging and infrastructure scaling
- S3-based ingestion: reads raw telemetry files from an S3 "incoming" folder
- Automated file detection: processes new S3 objects while skipping previously ingested files 

## Future Enhancements

- Data quality validation  
- Observability dashboards (CloudWatch, Grafana)  
- Data warehouse integration into Postgres
- Machine learning integration (anomaly detection)  

## Summary

This project demonstrates a complete data engineering workflow:

- Data ingestion and transformation  
- Pipeline orchestration  
- Containerization  
- CI/CD automation  
- Cloud deployment  
- Production debugging and infrastructure scaling  

It reflects real-world challenges and solutions, moving beyond simple pipelines into production-ready systems.
