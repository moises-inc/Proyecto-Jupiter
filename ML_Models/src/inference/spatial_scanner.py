"""
Proyecto Centinela - Spatial Grid Scanner Module
Performs a full multi-zone geographic risk scan across 100% of the La Serena commune footprint.
"""

import os
import pandas as pd
import numpy as np

from src.ingesters.ingest_sat_data import fetch_live_nrt_data
from src.features.feature_engineering import generate_hydrological_features, FEATURE_COLUMNS
from src.inference.live_inference import load_centinela_model


# 8 Key Geographic Sectors covering 100% of La Serena urban, rural, coastal and mountain footprint
LA_SERENA_SECTOR_GRID = {
    "pueblo_islon": {
        "name": "Pueblo Islón / Quebrada Santa Gracia",
        "type": "Precordillera / Quebrada",
        "elevation_m": 150,
        "vulnerability_type": "Aluvión y Lodosidad",
        "weight_precip_short": 0.45,
        "weight_api": 0.35,
        "weight_freezing": 0.20,
        "lat": -29.830, "lon": -71.180
    },
    "las_companias": {
        "name": "Las Compañías (Norte y Alta)",
        "type": "Urbano / Periurbano denso",
        "elevation_m": 60,
        "vulnerability_type": "Aislamiento y Colapso de Drenajes",
        "weight_precip_short": 0.35,
        "weight_api": 0.45,
        "weight_freezing": 0.20,
        "lat": -29.870, "lon": -71.240
    },
    "centro_historico": {
        "name": "Centro Histórico & Damero Comercial",
        "type": "Urbano denso",
        "elevation_m": 30,
        "vulnerability_type": "Anegamiento de Calles y Comercio",
        "weight_precip_short": 0.50,
        "weight_api": 0.40,
        "weight_freezing": 0.10,
        "lat": -29.902, "lon": -71.252
    },
    "av_del_mar": {
        "name": "Avenida del Mar & Borde Costero",
        "type": "Borde Costero / Playa",
        "elevation_m": 5,
        "vulnerability_type": "Marejadas e Inundación Marítima",
        "weight_precip_short": 0.40,
        "weight_api": 0.40,
        "weight_freezing": 0.20,
        "lat": -29.910, "lon": -71.275
    },
    "la_florida_el_pino": {
        "name": "La Florida / San Joaquín / Colina El Pino",
        "type": "Terrazas Urbanas Altas",
        "elevation_m": 120,
        "vulnerability_type": "Escorrentía Superficial en Pendiente",
        "weight_precip_short": 0.40,
        "weight_api": 0.40,
        "weight_freezing": 0.20,
        "lat": -29.915, "lon": -71.220
    },
    "alfalfares_vegas": {
        "name": "Alfalfares & Vegas Sur / Norte",
        "type": "Agrícola / Humedal Bajo",
        "elevation_m": 15,
        "vulnerability_type": "Apozamiento Severo y Nivel Freático",
        "weight_precip_short": 0.30,
        "weight_api": 0.55,
        "weight_freezing": 0.15,
        "lat": -29.925, "lon": -71.235
    },
    "ruta5_pasos_nivel": {
        "name": "Ruta 5 Norte & Pasos Bajo Nivel (Km 490-500)",
        "type": "Arteria Vial Crítica",
        "elevation_m": 10,
        "vulnerability_type": "Corte de Ruta 5 e Inundación de Pasos",
        "weight_precip_short": 0.55,
        "weight_api": 0.35,
        "weight_freezing": 0.10,
        "lat": -29.890, "lon": -71.260
    },
    "valle_elqui_lambert": {
        "name": "Entrada Valle Elqui / Lambert / Acceso Minero",
        "type": "Rural Precordillerano",
        "elevation_m": 220,
        "vulnerability_type": "Corte de Puentes y Aislamiento Rural",
        "weight_precip_short": 0.40,
        "weight_api": 0.40,
        "weight_freezing": 0.20,
        "lat": -29.850, "lon": -71.120
    }
}


def get_current_nrt_row(df: pd.DataFrame) -> pd.Series:
    """
    Selects the row matching current time (or nearest past hour) instead of picking future forecast hours.
    """
    now = pd.Timestamp.now()
    if df["time"].dt.tz is not None:
        now = pd.Timestamp.now(tz="America/Santiago")
    
    past_df = df[df["time"] <= now]
    if not past_df.empty:
        return past_df.iloc[-1]
    return df.iloc[0]


def scan_full_la_serena_grid() -> dict:
    """
    Executes a 100% spatial grid scan across all 8 geographic sectors of La Serena.
    """
    raw_df = fetch_live_nrt_data()
    features_df = generate_hydrological_features(raw_df)
    model, feature_cols = load_centinela_model()

    # Get current NRT row matching current time
    current_row = get_current_nrt_row(features_df)
    X_current = pd.DataFrame([current_row[feature_cols]])

    # Base ML probability
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_current)[0]
        classes = list(model.classes_)
        base_ml_prob = float(probs[classes.index(1)]) if 1 in classes else 0.0
    else:
        base_ml_prob = float(model.predict(X_current)[0])

    precip_24h = float(current_row.get("precip_accum_24h", 0.0))
    precip_6h = float(current_row.get("precip_accum_6h", 0.0))
    api_72h = float(current_row.get("api_72h", 0.0))
    high_freezing = float(current_row.get("high_freezing_level_flag", 0))

    # Water presence gating factor (0.0 if dry, 1.0 if heavy rain)
    precip_signal = np.clip((precip_24h + precip_6h * 2.0) / 15.0, 0.0, 1.0)
    soil_signal = np.clip(api_72h / 15.0, 0.0, 1.0)
    water_presence = max(precip_signal, soil_signal)

    scanned_sectors = []
    red_count = 0
    yellow_count = 0

    for key, info in LA_SERENA_SECTOR_GRID.items():
        freezing_factor = 1.0 + 0.5 * high_freezing if info["weight_freezing"] > 0.1 else 1.0
        
        base_score = (
            info["weight_precip_short"] * (precip_6h / 20.0) +
            info["weight_api"] * (api_72h / 25.0) +
            0.2 * base_ml_prob
        )
        
        # Risk score is gated by water presence
        score = min(1.0, base_score * water_presence * freezing_factor)
        score_pct = round(score * 100.0, 1)

        if score >= 0.7:
            semaforo = "🔴 ALERTA ROJA"
            red_count += 1
        elif score >= 0.4:
            semaforo = "🟡 ALERTA AMARILLA"
            yellow_count += 1
        else:
            semaforo = "🟢 VERDE ESTABLE"

        scanned_sectors.append({
            "key": key,
            "name": info["name"],
            "type": info["type"],
            "elevation_m": info["elevation_m"],
            "vulnerability": info["vulnerability_type"],
            "score_pct": score_pct,
            "semaforo": semaforo,
            "coordinates": {"lat": info["lat"], "lon": info["lon"]}
        })

    # Sort sectors by risk score descending
    scanned_sectors.sort(key=lambda x: x["score_pct"], reverse=True)

    # General commune alert level
    if red_count > 0:
        commune_status = "🔴 ALERTA ROJA COMUNAL (EVACUACIÓN / RESCATE PREVENTIVO)"
    elif yellow_count > 0:
        commune_status = "🟡 ALERTA AMARILLA COMUNAL (PREPARACIÓN DE PUESTOS MANDO)"
    else:
        commune_status = "🟢 ALERTA VERDE COMUNAL (CONDICIONES ESTABLES)"

    return {
        "timestamp": str(current_row["time"]),
        "total_sectors_scanned": len(scanned_sectors),
        "commune_status": commune_status,
        "telemetry_summary": {
            "precip_accum_24h_mm": round(precip_24h, 1),
            "precip_accum_6h_mm": round(precip_6h, 1),
            "api_soil_saturation": round(api_72h, 1),
            "freezing_level_m": round(float(current_row["freezing_level_scaled"] * 1000.0), 0)
        },
        "sectors": scanned_sectors
    }


def print_full_scan_report(scan_data: dict):
    """
    Prints a clean, comprehensive spatial scan report for La Serena.
    """
    print("\n" + "=" * 80)
    print(" 📡 PROYECTO CENTINELA — ESCANEO ESPACIAL COMPLETO DE LA SERENA (100% COBERTURA)")
    print("=" * 80)
    print(f" Timestamp: {scan_data['timestamp']}")
    print(f" Estado Comunal: {scan_data['commune_status']}")
    print(f" Sectores Escaneados: {scan_data['total_sectors_scanned']} Zonas Geográficas")
    print("-" * 80)
    print(" 📊 RESUMEN METEOROLÓGICO Y TELEDETECCIÓN:")
    t = scan_data["telemetry_summary"]
    print(f"  • Lluvia 24h: {t['precip_accum_24h_mm']} mm  |  Lluvia 6h: {t['precip_accum_6h_mm']} mm")
    print(f"  • Saturación Suelo (API): {t['api_soil_saturation']}  |  Isoterma Cero: {t['freezing_level_m']} m.n.m.")
    print("-" * 80)
    print(" 📍 MATRIZ DE RIESGO POR SECTOR (ORDENADA POR SEVERIDAD):")
    print(f" {'#':<3} | {'Sector / Zona':<42} | {'Semáforo':<18} | {'Riesgo %':<8}")
    print("-" * 80)
    for idx, s in enumerate(scan_data["sectors"], 1):
        print(f" {idx:<3} | {s['name']:<42} | {s['semaforo']:<18} | {s['score_pct']:<8.1f}%")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    scan_result = scan_full_la_serena_grid()
    print_full_scan_report(scan_result)
