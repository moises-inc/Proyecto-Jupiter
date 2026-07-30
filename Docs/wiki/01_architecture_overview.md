# 01. Architecture Overview

## Complete System Design

Proyecto Centinela is designed as a modular, real-time early warning system.

### Components
1. **Data Ingestion**: Collects satellite and hydrometeorological data.
2. **Feature Engineering**: Processes raw data into actionable features, utilizing hydrologic models like SCS-CN.
3. **ML Classifier**: A Random Forest model that predicts flood risks based on engineered features.
4. **Spatial Scanner**: Maps predictions across a 20-zone WGS84 grid.
5. **Dashboard**: Presents data via Real-Time NRT console and a Demo simulation environment.

## Data Flows
- Raw Data -> Ingestion Module -> Processed Data
- Processed Data -> Feature Engineering -> Feature Vectors
- Feature Vectors -> ML Model -> Risk Predictions
- Risk Predictions -> Spatial Scanner -> Zonal Alerts
- Zonal Alerts -> Dashboard -> User Interface
