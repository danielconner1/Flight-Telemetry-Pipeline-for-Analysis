# Flight Telemetry Data Pipeline

## Overview

This project builds an end-to-end data pipeline for processing aviation telemetry data. The goal is to transform raw flight sensor data into a structured, analysis-ready dataset suitable for downstream analytics and modeling.

The pipeline ingests raw telemetry files, standardizes time-series data, and generates flight-level features that capture both overall flight characteristics and dynamic behavior.

---

## Why this project

Telemetry data is inherently complex:

- Sensors operate at different sampling rates  
- Data includes both continuous signals (altitude, speed) and discrete states  
- Missing or noisy data is common  
- Raw data is not immediately suitable for analysis  

This project focuses on building a structured pipeline that:

- standardizes telemetry data  
- preserves signal fidelity  
- handles real-world data imperfections  
- produces consistent, model-ready outputs  

---

## Current Pipeline (Dagster-Orchestrated)

The pipeline is implemented using **Dagster**, which provides:

- asset-based pipeline modeling  
- dependency management  
- observability (logs, metadata, execution tracking)  
- reproducible execution  

Each stage is defined as a Dagster asset, forming a dependency graph:


## Architecture

```mermaid
flowchart TD
  A[Raw Telemetry Data] --> B[Ingest]
  B --> C[Process Time Series]
  C --> D[Feature Engineering]
  D --> E[Flight Summary Dataset]


## Future Work

### Dockerization
- Containerize the pipeline for consistent execution across environments  
- Standardize Python runtime, dependencies, and filesystem layout  
- Enable deployment to cloud or container-based platforms  

### CI/CD Integration
- Add automated pipeline validation using GitHub Actions or GitLab CI  
- Run linting and unit tests on every commit  
- Validate pipeline execution against a small sample dataset  
- Prevent regressions and ensure reproducibility  

### Monitoring & Alerting
- Add alerting for pipeline failures and data quality issues  
- Integrate logging and monitoring tools  
- Add alerting for pipeline failures and data quality issues  
- Integrate logging and monitoring tools  
- Improve observability for production usage  
