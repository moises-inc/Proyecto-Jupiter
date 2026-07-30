"""
Proyecto Centinela - Feature Engineering Module
Transforms raw satellite and meteorological time-series data into predictive hydrometeorological features.
"""

import pandas as pd
import numpy as np


def compute_antecedent_precipitation_index(series: pd.Series, decay_factor: float = 0.85) -> pd.Series:
    """
    Computes the Antecedent Precipitation Index (API):
    API_t = P_t + k * API_{t-1}
    Measures soil water retention and saturation over time.
    """
    api = np.zeros(len(series))
    values = series.fillna(0.0).values

    for i in range(1, len(values)):
        api[i] = values[i] + decay_factor * api[i - 1]

    return pd.Series(api, index=series.index)


def generate_hydrological_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes raw hourly weather/satellite DataFrame and engineers predictive features.
    """
    df = df.copy()
    df = df.sort_values("time").reset_index(drop=True)

    # Ensure numeric columns
    precip = df["precipitation"].fillna(0.0)

    # 1. Rolling Precipitation Accumulations
    df["precip_accum_1h"] = precip
    df["precip_accum_3h"] = precip.rolling(window=3, min_periods=1).sum()
    df["precip_accum_6h"] = precip.rolling(window=6, min_periods=1).sum()
    df["precip_accum_12h"] = precip.rolling(window=12, min_periods=1).sum()
    df["precip_accum_24h"] = precip.rolling(window=24, min_periods=1).sum()
    df["precip_accum_72h"] = precip.rolling(window=72, min_periods=1).sum()
    df["precip_accum_120h"] = precip.rolling(window=120, min_periods=1).sum()

    # 2. Short-term Intensity Deltas & Maxima
    df["precip_rate_3h_avg"] = df["precip_accum_3h"] / 3.0
    df["precip_max_1h_in_6h"] = precip.rolling(window=6, min_periods=1).max()

    # 3. Antecedent Precipitation Indices (Soil Saturation)
    df["api_24h"] = compute_antecedent_precipitation_index(precip, decay_factor=0.85)
    df["api_72h"] = compute_antecedent_precipitation_index(precip, decay_factor=0.92)

    # 4. Isoterma Cero (Freezing Level Height) Features
    if "freezing_level_height" in df.columns:
        freezing = df["freezing_level_height"].fillna(2500.0)
        # Flag if freezing level is above 3000m (liquid rain on high mountains)
        df["high_freezing_level_flag"] = (freezing > 3000.0).astype(int)
        df["freezing_level_scaled"] = freezing / 1000.0
    else:
        df["high_freezing_level_flag"] = 0
        df["freezing_level_scaled"] = 2.5

    # 5. Wind and Pressure features
    if "wind_speed_10m" in df.columns:
        df["wind_speed_10m"] = df["wind_speed_10m"].fillna(10.0)
    else:
        df["wind_speed_10m"] = 10.0

    if "surface_pressure" in df.columns:
        df["pressure_drop_6h"] = df["surface_pressure"].diff(6).fillna(0.0)
    else:
        df["pressure_drop_6h"] = 0.0

    # 6. Target Labels (Calculated for Ground Truth Training)
    # High runoff risk if heavy precipitation + saturated soil + high freezing level
    runoff_condition = (
        ((df["precip_accum_24h"] > 35.0) | (df["precip_accum_6h"] > 20.0)) &
        (df["api_72h"] > 25.0)
    )

    # Calculated risk score (0.0 to 1.0)
    norm_accum = np.clip(df["precip_accum_24h"] / 80.0, 0.0, 1.0)
    norm_api = np.clip(df["api_72h"] / 60.0, 0.0, 1.0)
    norm_freezing = np.clip((df["freezing_level_scaled"] - 2.5) / 1.5, 0.0, 1.0)

    raw_risk = 0.5 * norm_accum + 0.3 * norm_api + 0.2 * norm_freezing
    df["risk_score"] = np.clip(raw_risk, 0.0, 1.0)
    df["overflow_target"] = runoff_condition.astype(int)

    return df


FEATURE_COLUMNS = [
    "precip_accum_1h",
    "precip_accum_3h",
    "precip_accum_6h",
    "precip_accum_12h",
    "precip_accum_24h",
    "precip_accum_72h",
    "precip_accum_120h",
    "precip_rate_3h_avg",
    "precip_max_1h_in_6h",
    "api_24h",
    "api_72h",
    "high_freezing_level_flag",
    "freezing_level_scaled",
    "wind_speed_10m",
    "pressure_drop_6h"
]


if __name__ == "__main__":
    from src.ingesters.ingest_sat_data import fetch_open_meteo_data

    raw_df = fetch_open_meteo_data("2026-07-14", "2026-07-21")
    features_df = generate_hydrological_features(raw_df)
    print("Features engineered successfully.")
    print(features_df[FEATURE_COLUMNS + ["risk_score", "overflow_target"]].tail())
