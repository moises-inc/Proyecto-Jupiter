"""
Proyecto Centinela - Spatial Grid Scanner Module
Performs a 20-zone high-resolution geographic risk scan across 100% of La Serena footprint,
calibrated with pinpoint WGS84 coordinates for Pueblo Islón and Lambert, precise disaster classification,
and Estimated Time of Arrival (ETA) calculation.
"""

import os
import datetime
import pandas as pd
import numpy as np

from src.ingesters.ingest_sat_data import fetch_live_nrt_data
from src.features.feature_engineering import generate_hydrological_features, FEATURE_COLUMNS
from src.inference.live_inference import load_centinela_model


# 20 High-Resolution Geographic Sectors with exact calibrated WGS84 coordinates
LA_SERENA_SECTOR_GRID = {
    "pueblo_islon": {
        "name": "Pueblo Islón / Puente D-201",
        "type": "Precordillera / Ribereño",
        "elevation_m": 120, "radius_m": 1000,
        "disaster_type": "Aluvión y Escorrentía Detrítica en Quebrada",
        "concentration_time_hours": 1.5,
        "weight_precip_short": 0.50, "weight_api": 0.35, "weight_freezing": 0.15,
        "lat": -29.878, "lon": -71.218  # Pinpoint Pueblo Islón town center on D-201
    },
    "lambert_minero": {
        "name": "Lambert (Poblado y Escuela)",
        "type": "Precordillera / Minero",
        "elevation_m": 220, "radius_m": 1200,
        "disaster_type": "Aluvión en Quebrada y Aislamiento Rural",
        "concentration_time_hours": 1.5,
        "weight_precip_short": 0.45, "weight_api": 0.35, "weight_freezing": 0.20,
        "lat": -29.818, "lon": -71.148  # Pinpoint Lambert village center on D-201
    },
    "el_brillador_quebrada": {
        "name": "El Brillador & Quebrada Norte",
        "type": "Cerros y Quebradas Norte",
        "elevation_m": 310, "radius_m": 1400,
        "disaster_type": "Escorrentía Rápida en Ladera Minera",
        "concentration_time_hours": 1.2,
        "weight_precip_short": 0.50, "weight_api": 0.30, "weight_freezing": 0.20,
        "lat": -29.825, "lon": -71.175  # El Brillador hill district
    },
    "santa_gracia_alta": {
        "name": "Santa Gracia Alta / Pelícano",
        "type": "Alta Precordillera",
        "elevation_m": 380, "radius_m": 1600,
        "disaster_type": "Aluvión de Alta Quebrada",
        "concentration_time_hours": 1.0,
        "weight_precip_short": 0.50, "weight_api": 0.30, "weight_freezing": 0.20,
        "lat": -29.785, "lon": -71.130
    },
    "las_rojas": {
        "name": "Las Rojas & Entrada Precordillera",
        "type": "Valle Precordillerano",
        "elevation_m": 240, "radius_m": 1400,
        "disaster_type": "Aluvión en Quebrada y Corte Ruta D-41",
        "concentration_time_hours": 1.5,
        "weight_precip_short": 0.45, "weight_api": 0.35, "weight_freezing": 0.20,
        "lat": -29.970, "lon": -71.055
    },
    "algarrobito_gabriela": {
        "name": "Algarrobito / Gabriela Mistral / Quebrada Talca",
        "type": "Valle Ribereño Precordillerano",
        "elevation_m": 170, "radius_m": 1400,
        "disaster_type": "Escorrentía Detrítica y Crecida de Quebrada",
        "concentration_time_hours": 2.0,
        "weight_precip_short": 0.45, "weight_api": 0.40, "weight_freezing": 0.15,
        "lat": -29.960, "lon": -71.120
    },
    "altovalsol": {
        "name": "Altovalsol & Valle Medio",
        "type": "Rural Ribereño",
        "elevation_m": 110, "radius_m": 1200,
        "disaster_type": "Crecida de Cauce y Escorrentía Agrícola",
        "concentration_time_hours": 2.5,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.945, "lon": -71.165
    },
    "coquimbito_bellavista": {
        "name": "Coquimbito / Bellavista / Pan de Azúcar Norte",
        "type": "Agrícola Periurbano",
        "elevation_m": 85, "radius_m": 1200,
        "disaster_type": "Apozamiento Agrícola y Escorrentía de Faldeo",
        "concentration_time_hours": 3.0,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.955, "lon": -71.185
    },
    "las_companias_alta": {
        "name": "Las Compañías (Alta y Villa Lambert)",
        "type": "Urbano / Periurbano Denso",
        "elevation_m": 60, "radius_m": 1000,
        "disaster_type": "Aislamiento Territorial y Colapso Pluvial",
        "concentration_time_hours": 3.0,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.860, "lon": -71.240
    },
    "las_companias_baja": {
        "name": "Las Compañías (Baja y Sector Esmeralda)",
        "type": "Urbano Denso",
        "elevation_m": 40, "radius_m": 900,
        "disaster_type": "Anegamiento Vial Urbano y Colectores",
        "concentration_time_hours": 3.5,
        "weight_precip_short": 0.45, "weight_api": 0.45, "weight_freezing": 0.10,
        "lat": -29.875, "lon": -71.245
    },
    "compania_baja_ribereno": {
        "name": "Sector Ribereño Norte (Puentes Libertador / Zorrilla)",
        "type": "Urbano Ribereño Bajo",
        "elevation_m": 20, "radius_m": 800,
        "disaster_type": "Inundación por Desborde del Río Elqui",
        "concentration_time_hours": 4.0,
        "weight_precip_short": 0.35, "weight_api": 0.50, "weight_freezing": 0.15,
        "lat": -29.888, "lon": -71.250
    },
    "caleta_san_pedro": {
        "name": "Caleta San Pedro & Borde Norte",
        "type": "Costero / Borde Marítimo",
        "elevation_m": 8, "radius_m": 1200,
        "disaster_type": "Inundación Costera y Marejadas",
        "concentration_time_hours": 5.0,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.855, "lon": -71.275
    },
    "centro_historico": {
        "name": "Centro Histórico & Damero Comercial",
        "type": "Urbano Denso / Comercial",
        "elevation_m": 30, "radius_m": 800,
        "disaster_type": "Anegamiento de Colectores Pluviales",
        "concentration_time_hours": 3.5,
        "weight_precip_short": 0.55, "weight_api": 0.35, "weight_freezing": 0.10,
        "lat": -29.902, "lon": -71.252
    },
    "amunategui_mall": {
        "name": "Eje Av. Francisco de Aguirre / Amunátegui / Mall Plaza",
        "type": "Eje Comercial / Cívico",
        "elevation_m": 22, "radius_m": 800,
        "disaster_type": "Inundación de Colectores y Terminal de Buses",
        "concentration_time_hours": 3.5,
        "weight_precip_short": 0.55, "weight_api": 0.35, "weight_freezing": 0.10,
        "lat": -29.908, "lon": -71.256
    },
    "la_pampa": {
        "name": "La Pampa & Eje Av. Balmaceda",
        "type": "Urbano Residencial",
        "elevation_m": 45, "radius_m": 1000,
        "disaster_type": "Anegamiento Vial y Saturación de Colectores",
        "concentration_time_hours": 3.5,
        "weight_precip_short": 0.50, "weight_api": 0.40, "weight_freezing": 0.10,
        "lat": -29.920, "lon": -71.245
    },
    "el_milagro": {
        "name": "El Milagro & San Joaquín",
        "type": "Residencial Terraza Media",
        "elevation_m": 90, "radius_m": 1000,
        "disaster_type": "Escorrentía Superficial en Pendiente",
        "concentration_time_hours": 2.5,
        "weight_precip_short": 0.45, "weight_api": 0.40, "weight_freezing": 0.15,
        "lat": -29.930, "lon": -71.230
    },
    "cerro_grande": {
        "name": "Cerro Grande & Faldeos Este",
        "type": "Ladera / Faldeo",
        "elevation_m": 210, "radius_m": 1200,
        "disaster_type": "Escorrentía Rápida y Deslizamiento de Ladera",
        "concentration_time_hours": 1.5,
        "weight_precip_short": 0.50, "weight_api": 0.35, "weight_freezing": 0.15,
        "lat": -29.940, "lon": -71.210
    },
    "av_del_mar": {
        "name": "Avenida del Mar & Borde Costero Sur",
        "type": "Borde Costero / Playa",
        "elevation_m": 5, "radius_m": 1200,
        "disaster_type": "Inundación Costera y Salida de Esteros",
        "concentration_time_hours": 5.5,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.910, "lon": -71.275
    },
    "la_florida": {
        "name": "Sector La Florida / Aeródromo",
        "type": "Urbano / Servicios",
        "elevation_m": 65, "radius_m": 1000,
        "disaster_type": "Anegamiento Vial Urbano",
        "concentration_time_hours": 3.0,
        "weight_precip_short": 0.45, "weight_api": 0.45, "weight_freezing": 0.10,
        "lat": -29.915, "lon": -71.220
    },
    "ruta5_pasos_nivel": {
        "name": "Ruta 5 Norte & Pasos Bajo Nivel (Km 490-500)",
        "type": "Arteria Vial Crítica",
        "elevation_m": 10, "radius_m": 800,
        "disaster_type": "Corte de Ruta 5 e Inundación de Pasos Bajo Nivel",
        "concentration_time_hours": 4.0,
        "weight_precip_short": 0.55, "weight_api": 0.35, "weight_freezing": 0.10,
        "lat": -29.890, "lon": -71.260
    }
}


def get_current_nrt_row(df: pd.DataFrame) -> pd.Series:
    now = pd.Timestamp.now()
    if df["time"].dt.tz is not None:
        now = pd.Timestamp.now(tz="America/Santiago")
    
    past_df = df[df["time"] <= now]
    if not past_df.empty:
        return past_df.iloc[-1]
    return df.iloc[0]


def scan_full_la_serena_grid() -> dict:
    raw_df = fetch_live_nrt_data()
    features_df = generate_hydrological_features(raw_df)
    model, feature_cols = load_centinela_model()

    current_row = get_current_nrt_row(features_df)
    X_current = pd.DataFrame([current_row[feature_cols]])

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

    precip_signal = np.clip((precip_24h + precip_6h * 2.0) / 15.0, 0.0, 1.0)
    soil_signal = np.clip(api_72h / 15.0, 0.0, 1.0)
    water_presence = max(precip_signal, soil_signal)

    current_dt = pd.to_datetime(current_row["time"])

    scanned_sectors = []
    red_count = 0
    yellow_count = 0

    for key, info in LA_SERENA_SECTOR_GRID.items():
        freezing_factor = 1.5 if high_freezing == 1 and info["weight_freezing"] > 0.1 else 1.0
        
        base_score = (
            info["weight_precip_short"] * (precip_6h / 20.0) +
            info["weight_api"] * (api_72h / 25.0) +
            0.2 * base_ml_prob
        )
        
        score = min(1.0, base_score * water_presence * freezing_factor)
        score_pct = round(score * 100.0, 1)

        tc_hours = info["concentration_time_hours"]
        eta_time = current_dt + pd.Timedelta(hours=tc_hours)
        eta_formatted = eta_time.strftime("%H:%M hrs")

        if score >= 0.7:
            semaforo = "ALERTA ROJA"
            red_count += 1
        elif score >= 0.4:
            semaforo = "ALERTA AMARILLA"
            yellow_count += 1
        else:
            semaforo = "VERDE ESTABLE"

        scanned_sectors.append({
            "key": key,
            "name": info["name"],
            "type": info["type"],
            "elevation_m": info["elevation_m"],
            "radius_m": info["radius_m"],
            "disaster_type": info["disaster_type"],
            "concentration_time_hours": tc_hours,
            "eta_impact": eta_formatted,
            "score_pct": score_pct,
            "semaforo": semaforo,
            "coordinates": {"lat": info["lat"], "lon": info["lon"]}
        })

    scanned_sectors.sort(key=lambda x: x["score_pct"], reverse=True)

    if red_count > 0:
        commune_status = "ALERTA ROJA COMUNAL (EVACUACIÓN Y RESCATE PREVENTIVO ACTIVO)"
    elif yellow_count > 0:
        commune_status = "ALERTA AMARILLA COMUNAL (PREPARACIÓN DE PUESTOS DE MANDO)"
    else:
        commune_status = "ALERTA VERDE COMUNAL (CONDICIONES ESTABLES)"

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
