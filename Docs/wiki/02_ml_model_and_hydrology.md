# 02. ML Model and Hydrology

## Random Forest Model
The core predictive engine is a Random Forest classifier. This ensemble method provides high accuracy and handles non-linear relationships well, which is crucial for complex meteorological data.

## Feature Engineering
Features are derived from raw hydrometeorological data. Key engineered features include:
- Rainfall intensity (mm/hr)
- Cumulative rainfall
- Soil moisture index

## SCS Curve Number Hydrology
The Soil Conservation Service Curve Number (SCS-CN) method is used to estimate direct runoff from rainfall events. It takes into account:
- Soil type
- Land use
- Hydrologic condition

## Forecast Lead Time
The system calculates forecast lead times, allowing authorities to prepare. This includes predicting the ETA of the flood peak and the ETA of safe return (Calma) when waters recede to safe levels.
