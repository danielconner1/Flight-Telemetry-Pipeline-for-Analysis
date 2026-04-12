# Flight Telemetry Data Pipeline

## Overview

This project builds an end-to-end data pipeline for working with aviation telemetry data. The goal is to transform raw flight sensor data into a structured, analysis-ready dataset.

The pipeline processes raw telemetry files, standardizes time-series data, and generates flight-level features that capture both overall flight characteristics and dynamic behavior.

---

## Why this project

Telemetry data is inherently complex:

- Sensors operate at different rates  
- Data includes both continuous signals (altitude, speed) and discrete states  
- Raw data is not immediately suitable for analysis  

This project focuses on building a structured pipeline that:

- standardizes telemetry data  
- preserves signal fidelity  
- enables downstream analysis and modeling  

---

## What the pipeline currently does

### Ingest
- Converts raw telemetry data into Parquet format  
- Handles file-level processing and skip logic  

### Process
- Normalizes column names  
- Constructs a unified timestamp from date/time components  
- Sorts data chronologically  
- Removes invalid or incomplete records  

### Feature Engineering
- Aggregates time-series data into one row per flight  
- Generates summary features such as:
  - flight duration  
  - altitude statistics (max, mean, standard deviation, range)  
  - airspeed statistics (true and ground speed mean and variability)  
- Derives dynamic features capturing behavior over time:
  - climb rate (max and variability)  
  - speed change (max and variability)  

### Pipeline Execution
- Provides a pipeline runner to execute all stages: