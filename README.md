# Flight Telemetry Data Pipeline

## Overview

This project builds an end-to-end data pipeline for processing aviation telemetry data. The goal is to transform raw flight sensor data into a structured, analysis-ready dataset suitable for downstream analytics and modeling.

The pipeline ingests raw telemetry files, standardizes time-series data, and generates flight-level features that capture both overall flight characteristics and dynamic behavior.

The pipeline is orchestrated using Dagster and can be executed within a containerized environment.

---

## Why this project

Telemetry data is inherently complex:

- Sensors operate at different sampling rates
- Data includes both continuous signals, such as altitude and speed, and discrete states
- Missing or noisy data is common
- Raw data is not immediately suitable for analysis

This project focuses on building a structured, production-style pipeline that:

- standardizes telemetry data
- preserves signal fidelity
- handles real-world data imperfections
- produces consistent, model-ready outputs
- introduces orchestration, observability, and reproducibility

---

## Current Pipeline

The pipeline is orchestrated using Dagster. Each stage is defined as a Dagster asset, allowing the pipeline to be executed, monitored, and inspected through the Dagster UI.

Current asset flow:

ingest → process → features

Dagster provides:

- asset-based pipeline modeling
- dependency management
- execution logs
- run metadata
- selective or full pipeline materialization
- job-based execution and scheduling

A Dagster job groups all assets into a single executable pipeline.

---

## Pipeline Stages

### Ingest

The ingest stage converts raw telemetry CSV files into Parquet format.

Responsibilities:

- Read raw CSV telemetry files from the raw data directory
- Convert files to Parquet for better storage efficiency and downstream performance
- Skip files that have already been processed
- Track processed, skipped, and failed files

Output:

data/raw/parquet/

---

### Process

The process stage prepares raw Parquet telemetry files for analysis.

Responsibilities:

- Normalize column names
- Construct a unified timestamp from date and time components
- Sort each flight chronologically
- Remove invalid or incomplete records
- Write cleaned time-series files to the processed data directory

Output:

data/processed/parquet/

---

### Feature Engineering

The feature engineering stage aggregates processed time-series telemetry into one summary row per flight.

Generated features include:

- flight duration
- maximum altitude
- mean altitude
- altitude standard deviation
- altitude range
- true airspeed mean
- true airspeed standard deviation
- true airspeed range
- ground speed mean
- ground speed standard deviation
- dynamic behavior metrics such as climb rate and speed change

Output:

data/features/flight_summary.parquet

---

## Running the Pipeline

### Local Dagster Execution

cd orchestration  
dagster dev -m orchestration.definitions  

Open the Dagster UI:

http://localhost:3000

From the UI you can:

- materialize individual assets
- run the full pipeline via job
- inspect logs
- review execution metadata
- troubleshoot failed stages

---

### Docker Execution

Build and run the container:

docker build -t telemetry-pipeline .  
docker run --rm -p 3000:3000 telemetry-pipeline  

Open:

http://localhost:3000

This provides a consistent runtime environment and mirrors production-style execution.

---

## Architecture

Raw Telemetry CSV Files  
→ Ingest  
→ Raw Parquet Files  
→ Process Time Series  
→ Processed Parquet Files  
→ Feature Engineering  
→ Flight Summary Dataset  

---

## Orchestration and Execution Model

- Assets define pipeline stages and dependencies
- Jobs group assets into executable pipelines
- Dagster UI provides observability into runs and asset lineage
- Docker ensures environment consistency and portability

---

## Design Principles

- Modular stages with clear responsibilities
- Idempotent processing to support safe re-runs
- Separation of concerns between ingestion, processing, and features
- Observability through Dagster logs and metadata
- Reproducibility via Dockerized execution
- Extensibility for future enhancements

---

## Current Capabilities

- End-to-end telemetry pipeline from raw data to feature dataset
- Asset-based orchestration using Dagster
- Job-based execution model
- Local and containerized execution support
- Pipeline observability through Dagster UI
- Scheduled execution using Dagster schedules and daemon

---

## Future Work

---

### CI/CD Integration

- Add GitHub Actions for automated validation
- Run dependency installation and pipeline validation on commit

---

## Summary

This project demonstrates a production-oriented data pipeline built with Python, orchestrated using Dagster, and executed in a containerized environment.

The pipeline transforms raw telemetry data into structured, feature-rich datasets while maintaining modularity, reproducibility, and scalability.

Future enhancements will focus on scheduling, CI/CD automation, persistence, data quality validation, and scalable execution.
