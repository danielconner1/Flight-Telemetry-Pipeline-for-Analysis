# Flight Telemetry Data Pipeline

## Overview

This project builds a data pipeline for working with aviation telemetry data. The goal is to take raw flight sensor data and turn it into something you can actually analyze.

The dataset includes a mix of signals collected at different rates (engine data, flight controls, system states, etc.), so a big part of the pipeline is getting everything aligned on a consistent timeline. From there, the pipeline standardizes the data, derives useful features (like flight phases and engine comparisons), and outputs datasets that are easier to query and explore.

---

## Why this project

Telemetry data is messy. Different sensors behave differently, update at different rates, and don’t always line up cleanly. You also have a mix of:

- continuous values (altitude, speed, engine temperature)
- discrete states (gear, flaps, weight-on-wheels)

Each type needs to be handled differently to avoid introducing bad data.

This project focuses on building a simple but structured pipeline that moves raw telemetry data through validation, normalization, and feature engineering so it can be used for analysis or future modeling.

---

## What the pipeline does

- Ingests raw flight telemetry files
- Validates schema and basic data quality
- Standardizes column names and data types
- Aligns multi-rate sensor data to a common time index
- Applies:
  - interpolation for continuous signals
  - forward-fill for discrete/state signals
- Derives features such as:
  - flight phases
  - engine performance metrics
  - engine-to-engine comparisons
- Flags anomaly candidates (e.g., engine imbalance)
- Outputs analytics-ready datasets (Parquet + DuckDB)

---

## Architecture

```mermaid
flowchart TD
    A[Raw Telemetry Data] --> B[Ingest and Validate]
    B --> C[Normalize Time Series]
    C --> D[Feature Engineering]
    D --> E[Analytics Ready Data]
    E --> F[Query Analysis ML]
