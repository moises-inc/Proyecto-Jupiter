"""
Proyecto Centinela - Live NRT Inference Module
Executes real-time predictions for La Serena Command Post & Firefighters.
"""

import os
import joblib
import pandas as pd
import numpy as np

from src.ingesters.ingest_sat_data import fetch_live_nrt_data
from src.features.feature_engineering import generate_hydrological_features, FEATURE_COLUMNS


MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "trained_models",
    "centinela_sat_v1.joblib"
)


def load_centinela_model(path: str = MODEL_PATH):
    """
    Loads serialized ML model artifact.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Serialized model artifact not found at '{path}'. Please run train_flood_predictor.py first.")
    
    artifact = joblib.load(path)
    return artifact["model"], artifact.get("feature_columns", FEATURE_COLUMNS)


def evaluate_sector_tactical_risks(latest_row: pd.Series, risk_score: float) -> dict:
    """
    Translates macro satellite risk predictions into localized sector semáforos for La Serena.
    """
    precip_24h = latest_row.get("precip_accum_24h", 0.0)
    precip_6h = latest_row.get("precip_accum_6h", 0.0)
    api_72h = latest_row.get("api_72h", 0.0)
    high_freezing = latest_row.get("high_freezing_level_flag", 0)

    # Sector 1: Pueblo Islón / Quebrada Santa Gracia (Aluvión)
    pueblo_islon_score = min(1.0, 0.4 * (precip_6h / 20.0) + 0.4 * (api_72h / 25.0) + 0.2 * high_freezing)
    if pueblo_islon_score >= 0.7:
        islon_semaforo = "ROJO - RIESGO INMINENTE DE ALUVIÓN"
    elif pueblo_islon_score >= 0.4:
        islon_semaforo = "AMARILLO - PRE-ALERTA Y PREPARACIÓN"
    else:
        islon_semaforo = "VERDE - CONDICIÓN ESTABLE"

    # Sector 2: Las Compañías / El Islón (Aislamiento e Inundación)
    las_companias_score = min(1.0, 0.5 * (precip_24h / 35.0) + 0.5 * (api_72h / 30.0))
    if las_companias_score >= 0.7:
        companias_semaforo = "ROJO - RIESGO DE AISLAMIENTO Y DESBORDE"
    elif las_companias_score >= 0.4:
        companias_semaforo = "AMARILLO - MONITOREO DE CAUCE"
    else:
        companias_semaforo = "VERDE - CONDICIÓN ESTABLE"

    # Sector 3: La Serena Urbana / Ruta 5 Km 499 (Inundación Vial)
    urbana_score = min(1.0, 0.6 * (precip_6h / 25.0) + 0.4 * (precip_24h / 40.0))
    if urbana_score >= 0.7:
        urbana_semaforo = "ROJO - ANAGAMIENTO RUTA 5 Y COLECTORES"
    elif urbana_score >= 0.4:
        urbana_semaforo = "AMARILLO - TRÁNSITO CON PRECAUCIÓN"
    else:
        urbana_semaforo = "VERDE - TRÁNSITO NORMAL"

    # Overall General Semáforo
    if risk_score >= 0.7 or islon_semaforo.startswith("ROJO"):
        general_semaforo = "🔴 ALERTA ROJA (EVACUACIÓN / PREVENCIÓN ACTIVA)"
    elif risk_score >= 0.4 or islon_semaforo.startswith("AMARILLO"):
        general_semaforo = "🟡 ALERTA AMARILLA (PREPARACIÓN PUESTOS MANDO)"
    else:
        general_semaforo = "🟢 ALERTA VERDE (ESTABLE)"

    return {
        "general_semaforo": general_semaforo,
        "overall_risk_score_pct": round(risk_score * 100, 1),
        "sectors": {
            "pueblo_islon": {
                "name": "Pueblo Islón / Quebrada Santa Gracia",
                "semaforo": islon_semaforo,
                "score_pct": round(pueblo_islon_score * 100, 1)
            },
            "las_companias": {
                "name": "Las Compañías / El Islón",
                "semaforo": companias_semaforo,
                "score_pct": round(las_companias_score * 100, 1)
            },
            "la_serena_urbana": {
                "name": "La Serena Urbana / Ruta 5 Km 499",
                "semaforo": urbana_semaforo,
                "score_pct": round(urbana_score * 100, 1)
            }
        }
    }


def run_live_inference() -> dict:
    """
    Executes end-to-end live inference pipeline:
    1. Fetches NRT satellite/weather data.
    2. Computes features.
    3. Runs ML model prediction.
    4. Generates tactical bulletin.
    """
    print("Fetching NRT Satellite Data for La Serena...")
    raw_df = fetch_live_nrt_data()
    features_df = generate_hydrological_features(raw_df)

    model, feature_cols = load_centinela_model()

    # Get latest timestamp row
    latest_row = features_df.iloc[-1]
    X_latest = pd.DataFrame([latest_row[feature_cols]])

    # Predict risk safely across classes
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_latest)[0]
        classes = list(model.classes_)
        if 1 in classes:
            idx = classes.index(1)
            model_prob = float(probs[idx])
        else:
            model_prob = 0.0
    else:
        model_prob = float(model.predict(X_latest)[0])

    # Blend model probability with continuous hydrological feature risk_score
    feature_risk = float(latest_row.get("risk_score", 0.0))
    risk_prob = max(model_prob, feature_risk)

    tactic = evaluate_sector_tactical_risks(latest_row, risk_prob)

    bulletin = {
        "timestamp": str(latest_row["time"]),
        "telemetry_metrics": {
            "precip_accum_24h_mm": round(float(latest_row["precip_accum_24h"]), 1),
            "precip_accum_6h_mm": round(float(latest_row["precip_accum_6h"]), 1),
            "api_soil_saturation_72h": round(float(latest_row["api_72h"]), 1),
            "freezing_level_m": round(float(latest_row["freezing_level_scaled"] * 1000.0), 0),
            "high_freezing_level_flag": int(latest_row["high_freezing_level_flag"])
        },
        "tactic": tactic
    }

    return bulletin


def print_formatted_bulletin(bulletin: dict):
    """
    Prints a clean, human-readable emergency bulletin for command post operators.
    """
    print("\n" + "=" * 65)
    print(" 📡 PROYECTO CENTINELA — BOLETÍN TÁCTICO DE EMERGENCIAS (LA SERENA)")
    print("=" * 65)
    print(f" Timestamp: {bulletin['timestamp']}")
    print(f" Estado General: {bulletin['tactic']['general_semaforo']}")
    print(f" Score Global de Riesgo ML: {bulletin['tactic']['overall_risk_score_pct']}%")
    print("-" * 65)
    print(" 📊 TELEMETRÍA SATELITAL & HIDROLÓGICA (NRT):")
    metrics = bulletin['telemetry_metrics']
    print(f"  • Precipitación Acumulada 24h: {metrics['precip_accum_24h_mm']} mm")
    print(f"  • Precipitación Acumulada 6h:  {metrics['precip_accum_6h_mm']} mm")
    print(f"  • Saturación de Suelo (API):   {metrics['api_soil_saturation_72h']}")
    print(f"  • Altitud Isoterma Cero:      {metrics['freezing_level_m']} m.n.m.")
    print("-" * 65)
    print(" 📍 ESTADO POR SECTOR (LA SERENA):")
    for sec_key, sec in bulletin['tactic']['sectors'].items():
        print(f"  • {sec['name']}: {sec['semaforo']} ({sec['score_pct']}%)")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    bulletin = run_live_inference()
    print_formatted_bulletin(bulletin)
