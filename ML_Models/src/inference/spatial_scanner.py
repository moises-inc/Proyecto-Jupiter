"""
Proyecto Júpiter - Spatial Grid Scanner Module (v5.0)
Performs a 20-zone high-resolution geographic risk scan across 100% of La Serena footprint,
calibrated with pinpoint WGS84 coordinates for Pueblo Islón and Lambert, SCS-CN hydrology,
forecast lead-times (+1h/+3h/+6h), ETA of Impact, and ETA of Safe Return (Calma / Transitabilidad).
"""

import os
import datetime
import pandas as pd
import numpy as np

from src.ingesters.ingest_sat_data import fetch_live_nrt_data
from src.ingesters.ingest_ceazamet import get_ceazamet_ground_truth_summary
from src.ingesters.ingest_senapred import get_chilean_agencies_summary
from src.features.feature_engineering import generate_hydrological_features, FEATURE_COLUMNS
from src.inference.live_inference import load_jupiter_model


# Persistent Global EMA State Memory for Risk Scores (Prevents alert flickering)
PREVIOUS_SCORES_EMA = {}
PREVIOUS_SEMAFORO_STATE = {}


def calculate_scs_direct_runoff(precip_24h_mm: float, cn: float) -> float:
    if precip_24h_mm <= 0.0 or cn <= 0:
        return 0.0
    S = (25400.0 / cn) - 254.0
    Ia = 0.2 * S
    if precip_24h_mm <= Ia:
        return 0.0
    P_minus_Ia = precip_24h_mm - Ia
    return (P_minus_Ia ** 2) / (precip_24h_mm + 0.8 * S)


def get_current_nrt_row(features_df: pd.DataFrame) -> pd.Series:
    now_dt = datetime.datetime.now()
    if "time" in features_df.columns:
        past_df = features_df[features_df["time"] <= now_dt]
        if not past_df.empty:
            return past_df.iloc[-1]
    return features_df.iloc[-1]


def scan_full_la_serena_grid() -> dict:
    global PREVIOUS_SCORES_EMA, PREVIOUS_SEMAFORO_STATE

    raw_df = fetch_live_nrt_data()
    features_df = generate_hydrological_features(raw_df)
    model, feature_cols = load_jupiter_model()
    current_row = get_current_nrt_row(features_df)
    valid_cols = [col for col in feature_cols if col in current_row.index]
    X_current = pd.DataFrame([[current_row[c] for c in valid_cols]], columns=valid_cols)

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

    forecast_1h = float(current_row.get("precip_forecast_1h", 0.0))
    forecast_3h = float(current_row.get("precip_forecast_3h", 0.0))
    forecast_6h = float(current_row.get("precip_forecast_6h", 0.0))
    forecast_12h = float(current_row.get("precip_forecast_12h", 0.0))
    forecast_24h = float(current_row.get("precip_forecast_24h", 0.0))

    nowcast_rate = float(current_row.get("nowcast_rain_rate", 0.0))
    geotech_fs = float(current_row.get("geotech_fs", 2.0))
    muskingum_q = float(current_row.get("muskingum_cunge_q", 0.0))
    phys_constraint = float(current_row.get("physics_informed_constraint", 0.0))
    enkf_corr = float(current_row.get("enkf_assimilation_correction", 0.0))

    # Blend with CEAZAMET ground-truth observations in real-time
    _, ceazamet_summary = get_ceazamet_ground_truth_summary()
    if ceazamet_summary.get("ceazamet_available"):
        obs_peak = float(ceazamet_summary.get("peak_precipitation_mm", 0.0))
        obs_avg = float(ceazamet_summary.get("communal_avg_precipitation_mm", 0.0))
        ground_obs = max(obs_peak, obs_avg)
        nowcast_rate = max(nowcast_rate, ground_obs)
        enkf_corr = max(enkf_corr, ground_obs)
        precip_24h = max(precip_24h, ground_obs)
        precip_6h = max(precip_6h, ground_obs)

    # Chilean Official Agencies Data Ingestion (SENAPRED & DMC)
    agency_summary = get_chilean_agencies_summary()

    # Continuous Logistic Ceiling C(P_24h) in [0.25, 1.0]
    # Prevents false alarms during light drizzle while scaling smoothly during heavy storms
    logistic_ceiling = 0.25 + (0.75 / (1.0 + np.exp(-0.25 * (precip_24h - 15.0))))

    current_dt = pd.to_datetime(current_row["time"])
    scanned_sectors = []
    red_count = 0
    yellow_count = 0

    for key, info in LA_SERENA_SECTOR_GRID.items():
        cn = info.get("scs_cn", 80)
        direct_Q = calculate_scs_direct_runoff(precip_24h, cn)
        freezing_factor = 1.3 if high_freezing == 1 and info["weight_freezing"] > 0.1 else 1.0

        # 1. Convex Normalized Base Score (Sum of weights = 1.00)
        phi_precip = min(1.0, precip_6h / 25.0)
        phi_api = min(1.0, api_72h / 40.0)
        phi_ml = base_ml_prob
        
        # Effective Hydro Runoff: Accounts for both local SCS runoff AND upstream river surge (Muskingum / EnKF)
        effective_hydro_q = max(direct_Q, muskingum_q, enkf_corr)
        phi_runoff = min(1.0, effective_hydro_q / 10.0)
        phi_forecast = 0.4 * min(1.0, forecast_3h / 15.0) + 0.6 * min(1.0, forecast_6h / 20.0)
        phi_geotech = 1.0 / (1.0 + np.exp(8.0 * (geotech_fs - 1.0)))
        phi_routing = min(1.0, muskingum_q / 25.0)

        raw_convex_score = (
            0.25 * phi_precip +
            0.20 * phi_api +
            0.15 * phi_ml +
            0.15 * phi_runoff +
            0.15 * phi_forecast +
            0.05 * phi_geotech +
            0.05 * phi_routing
        )

        # Precordillera / River Quebrada Special Weighting
        is_river_quebrada = info["type"] in [
            "Precordillera / Ribereño", "Alta Precordillera", "Quebrada Norte", 
            "Valle Precordillerano", "Cerros y Quebradas Norte", "Rural Interior"
        ]
        
        if is_river_quebrada and (effective_hydro_q >= 2.0 or enkf_corr >= 5.0):
            # Upstream river surge or mountain storm active -> boost precordillera risk score
            raw_convex_score = max(raw_convex_score, 0.75)

        # 2. Apply Continuous Logistic Ceiling and Freezing Factor
        inst_score = min(1.0, raw_convex_score * logistic_ceiling * freezing_factor)

        # 3. Asymmetric Adaptive EMA Temporal Smoothing
        prev_ema = PREVIOUS_SCORES_EMA.get(key, inst_score)
        if inst_score >= prev_ema:
            alpha = 0.45  # Rapid adaptation when risk increases
        else:
            alpha = 0.10  # Gradual decay memory when storm recedes

        smooth_score = alpha * inst_score + (1.0 - alpha) * prev_ema
        PREVIOUS_SCORES_EMA[key] = smooth_score

        # 4. Inviolable Physical Safety Safeguard Rules
        # Exception: Do NOT cap river/quebrada sectors if upstream river surge is active (effective_hydro_q >= 2.0)
        if not (is_river_quebrada and effective_hydro_q >= 2.0):
            if precip_24h < 10.0 and effective_hydro_q < 1.0 and geotech_fs >= 1.0:
                smooth_score = min(smooth_score, 0.25)
            elif precip_24h < 25.0 and effective_hydro_q < 5.0 and geotech_fs >= 1.0:
                smooth_score = min(smooth_score, 0.55)

        score_pct = round(smooth_score * 100.0, 1)

        # 5. Alert Hysteresis Bands (8% Buffer)
        prev_state = PREVIOUS_SEMAFORO_STATE.get(key, "VERDE ESTABLE")
        if prev_state == "ALERTA ROJA":
            if smooth_score < 0.62:
                semaforo = "ALERTA AMARILLA" if smooth_score >= 0.33 else "VERDE ESTABLE"
            else:
                semaforo = "ALERTA ROJA"
        elif prev_state == "ALERTA AMARILLA":
            if smooth_score >= 0.70:
                semaforo = "ALERTA ROJA"
            elif smooth_score < 0.33:
                semaforo = "VERDE ESTABLE"
            else:
                semaforo = "ALERTA AMARILLA"
        else:
            if smooth_score >= 0.70:
                semaforo = "ALERTA ROJA"
            elif smooth_score >= 0.40:
                semaforo = "ALERTA AMARILLA"
            else:
                semaforo = "VERDE ESTABLE"

        PREVIOUS_SEMAFORO_STATE[key] = semaforo

        tc_hours = info["concentration_time_hours"]
        drain_hours = info.get("recovery_drain_hours", 2.0)

        # Dynamic Forecast Peak & Safe Clearance Scanning
        future_df = features_df[features_df["time"] >= current_dt]
        active_rain_df = future_df[future_df["precipitation"] > 0.1]

        if not active_rain_df.empty:
            peak_idx = active_rain_df["precipitation"].idxmax()
            peak_forecast_dt = pd.to_datetime(active_rain_df.loc[peak_idx, "time"])
            eta_impact = peak_forecast_dt + pd.Timedelta(hours=tc_hours)
            eta_impact_formatted = eta_impact.strftime("%d/%m/%Y %H:%M hrs")

            last_rain_dt = pd.to_datetime(active_rain_df["time"].iloc[-1])
            eta_safe_return = last_rain_dt + pd.Timedelta(hours=drain_hours)
            eta_safe_formatted = eta_safe_return.strftime("%d/%m/%Y %H:%M hrs")
        elif smooth_score > 0.3:
            eta_impact = current_dt + pd.Timedelta(hours=tc_hours)
            eta_impact_formatted = eta_impact.strftime("%d/%m/%Y %H:%M hrs")
            eta_safe_return = eta_impact + pd.Timedelta(hours=drain_hours + 2.0)
            eta_safe_formatted = eta_safe_return.strftime("%d/%m/%Y %H:%M hrs")
        else:
            eta_impact_formatted = "Sin Lluvia Prevista"
            eta_safe_formatted = "Condición Estable (Transitable)"

        if semaforo == "ALERTA ROJA":
            transitability = f"TRANSITO RESTRICTORIO (Hora de Paso Seguro (Calma): {eta_safe_formatted})"
            red_count += 1
        elif semaforo == "ALERTA AMARILLA":
            transitability = f"PRECAUCIÓN VIAL (Hora de Paso Seguro (Calma): {eta_safe_formatted})"
            yellow_count += 1
        else:
            transitability = "TRANSITABLE (Condición Normal)"

        scanned_sectors.append({
            "key": key,
            "name": info["name"],
            "type": info["type"],
            "elevation_m": info["elevation_m"],
            "radius_m": info["radius_m"],
            "disaster_type": info["disaster_type"],
            "concentration_time_hours": tc_hours,
            "recovery_drain_hours": drain_hours,
            "eta_impact": eta_impact_formatted,
            "eta_safe_return": eta_safe_formatted,
            "transitability_status": transitability,
            "scs_curve_number": cn,
            "agua_acumulada_superficie": round(direct_Q, 2),
            "forecast_1h": round(forecast_1h, 1),
            "forecast_3h": round(forecast_3h, 1),
            "forecast_6h": round(forecast_6h, 1),
            "forecast_12h": round(forecast_12h, 1),
            "forecast_24h": round(forecast_24h, 1),
            "score_pct": score_pct,
            "geotech_fs": round(geotech_fs, 2),
            "nowcast_rain_rate": round(nowcast_rate, 2),
            "muskingum_q": round(muskingum_q, 2),
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
        "ceazamet_telemetry": ceazamet_summary,
        "chilean_official_agencies": agency_summary,
        "sectors": scanned_sectors
    }


# 20 High-Resolution Geographic Sectors with calibrated WGS84, SCS-CN, and Clearance Recovery times
LA_SERENA_SECTOR_GRID = {
    "pueblo_islon": {
        "name": "Pueblo Islón / Quebrada Santa Gracia",
        "type": "Precordillera / Ribereño",
        "elevation_m": 120, "radius_m": 1000,
        "disaster_type": "Aluvión y Escorrentía Detrítica en Quebrada",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 2.5,  # Hours post-peak to achieve safe clearance
        "scs_cn": 88,
        "weight_precip_short": 0.50, "weight_api": 0.35, "weight_freezing": 0.15,
        "lat": -29.878, "lon": -71.218
    },
    "lambert_minero": {
        "name": "Lambert & Acceso Minero Norte",
        "type": "Precordillera / Minero",
        "elevation_m": 220, "radius_m": 1200,
        "disaster_type": "Aluvión en Quebrada y Aislamiento Rural",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 2.5,
        "scs_cn": 88,
        "weight_precip_short": 0.45, "weight_api": 0.35, "weight_freezing": 0.20,
        "lat": -29.818, "lon": -71.148
    },
    "el_brillador_quebrada": {
        "name": "El Brillador & Quebrada Norte",
        "type": "Cerros y Quebradas Norte",
        "elevation_m": 310, "radius_m": 1400,
        "disaster_type": "Escorrentía Rápida en Ladera Minera",
        "concentration_time_hours": 1.2,
        "recovery_drain_hours": 2.0,
        "scs_cn": 88,
        "weight_precip_short": 0.50, "weight_api": 0.30, "weight_freezing": 0.20,
        "lat": -29.825, "lon": -71.175
    },
    "santa_gracia_alta": {
        "name": "Santa Gracia Alta / Pelícano",
        "type": "Alta Precordillera",
        "elevation_m": 380, "radius_m": 1600,
        "disaster_type": "Aluvión de Alta Quebrada",
        "concentration_time_hours": 1.0,
        "recovery_drain_hours": 2.0,
        "scs_cn": 88,
        "weight_precip_short": 0.50, "weight_api": 0.30, "weight_freezing": 0.20,
        "lat": -29.785, "lon": -71.130
    },
    "las_rojas": {
        "name": "Las Rojas & Entrada Precordillera",
        "type": "Valle Precordillerano",
        "elevation_m": 240, "radius_m": 1400,
        "disaster_type": "Aluvión en Quebrada y Corte Ruta D-41",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 3.0,
        "scs_cn": 88,
        "weight_precip_short": 0.45, "weight_api": 0.35, "weight_freezing": 0.20,
        "lat": -29.970, "lon": -71.055
    },
    "algarrobito_gabriela": {
        "name": "Algarrobito / Gabriela Mistral / Quebrada Talca",
        "type": "Valle Ribereño Precordillerano",
        "elevation_m": 170, "radius_m": 1400,
        "disaster_type": "Escorrentía Detrítica y Crecida de Quebrada",
        "concentration_time_hours": 2.0,
        "recovery_drain_hours": 3.0,
        "scs_cn": 85,
        "weight_precip_short": 0.45, "weight_api": 0.40, "weight_freezing": 0.15,
        "lat": -29.960, "lon": -71.120
    },
    "altovalsol": {
        "name": "Altovalsol & Valle Medio",
        "type": "Rural Ribereño",
        "elevation_m": 110, "radius_m": 1200,
        "disaster_type": "Crecida de Cauce y Escorrentía Agrícola",
        "concentration_time_hours": 2.5,
        "recovery_drain_hours": 3.5,
        "scs_cn": 75,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.945, "lon": -71.165
    },
    "coquimbito_bellavista": {
        "name": "Coquimbito / Bellavista / Pan de Azúcar Norte",
        "type": "Agrícola Periurbano",
        "elevation_m": 85, "radius_m": 1200,
        "disaster_type": "Apozamiento Agrícola y Escorrentía de Faldeo",
        "concentration_time_hours": 2.5,
        "recovery_drain_hours": 3.5,
        "scs_cn": 75,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.955, "lon": -71.185
    },
    "las_companias_alta": {
        "name": "Las Compañías (Alta y Villa Lambert)",
        "type": "Urbano / Periurbano Denso",
        "elevation_m": 60, "radius_m": 1000,
        "disaster_type": "Aislamiento Territorial y Colapso Pluvial",
        "concentration_time_hours": 2.0,
        "recovery_drain_hours": 2.5,
        "scs_cn": 90,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.860, "lon": -71.240
    },
    "las_companias_baja": {
        "name": "Las Compañías (Baja y Sector Esmeralda)",
        "type": "Urbano Denso",
        "elevation_m": 40, "radius_m": 900,
        "disaster_type": "Anegamiento Vial Urbano y Colectores",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 2.0,
        "scs_cn": 90,
        "weight_precip_short": 0.45, "weight_api": 0.45, "weight_freezing": 0.10,
        "lat": -29.875, "lon": -71.245
    },
    "compania_baja_ribereno": {
        "name": "Sector Ribereño Norte (Puentes Libertador / Zorrilla)",
        "type": "Urbano Ribereño Bajo",
        "elevation_m": 20, "radius_m": 800,
        "disaster_type": "Inundación por Desborde del Río Elqui",
        "concentration_time_hours": 4.0,
        "recovery_drain_hours": 5.0,  # River flooding takes longer to recede
        "scs_cn": 85,
        "weight_precip_short": 0.35, "weight_api": 0.50, "weight_freezing": 0.15,
        "lat": -29.888, "lon": -71.250
    },
    "caleta_san_pedro": {
        "name": "Caleta San Pedro & Borde Norte",
        "type": "Costero / Borde Marítimo",
        "elevation_m": 8, "radius_m": 1200,
        "disaster_type": "Inundación Costera y Marejadas",
        "concentration_time_hours": 5.0,
        "recovery_drain_hours": 4.0,
        "scs_cn": 70,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.855, "lon": -71.275
    },
    "centro_historico": {
        "name": "Centro Histórico & Damero Comercial",
        "type": "Urbano Denso / Comercial",
        "elevation_m": 30, "radius_m": 800,
        "disaster_type": "Anegamiento de Colectores Pluviales",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 1.5,  # Urban drains flush relatively fast after rain stops
        "scs_cn": 92,
        "weight_precip_short": 0.55, "weight_api": 0.35, "weight_freezing": 0.10,
        "lat": -29.902, "lon": -71.252
    },
    "amunategui_mall": {
        "name": "Eje Av. Francisco de Aguirre / Amunátegui / Mall Plaza",
        "type": "Eje Comercial / Cívico",
        "elevation_m": 22, "radius_m": 800,
        "disaster_type": "Inundación de Colectores y Terminal de Buses",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 1.5,
        "scs_cn": 92,
        "weight_precip_short": 0.55, "weight_api": 0.35, "weight_freezing": 0.10,
        "lat": -29.908, "lon": -71.256
    },
    "la_pampa": {
        "name": "La Pampa & Eje Av. Balmaceda",
        "type": "Urbano Residencial",
        "elevation_m": 45, "radius_m": 1000,
        "disaster_type": "Anegamiento Vial y Saturación de Colectores",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 2.0,
        "scs_cn": 88,
        "weight_precip_short": 0.50, "weight_api": 0.40, "weight_freezing": 0.10,
        "lat": -29.920, "lon": -71.245
    },
    "el_milagro": {
        "name": "El Milagro & San Joaquín",
        "type": "Residencial Terraza Media",
        "elevation_m": 90, "radius_m": 1000,
        "disaster_type": "Escorrentía Superficial en Pendiente",
        "concentration_time_hours": 2.0,
        "recovery_drain_hours": 1.5,
        "scs_cn": 85,
        "weight_precip_short": 0.45, "weight_api": 0.40, "weight_freezing": 0.15,
        "lat": -29.930, "lon": -71.230
    },
    "cerro_grande": {
        "name": "Cerro Grande & Faldeos Este",
        "type": "Ladera / Faldeo",
        "elevation_m": 210, "radius_m": 1200,
        "disaster_type": "Escorrentía Rápida y Deslizamiento de Ladera",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 2.0,
        "scs_cn": 88,
        "weight_precip_short": 0.50, "weight_api": 0.35, "weight_freezing": 0.15,
        "lat": -29.940, "lon": -71.210
    },
    "av_del_mar": {
        "name": "Avenida del Mar & Borde Costero Sur",
        "type": "Borde Costero / Playa",
        "elevation_m": 5, "radius_m": 1200,
        "disaster_type": "Inundación Costera y Salida de Esteros",
        "concentration_time_hours": 5.0,
        "recovery_drain_hours": 4.5,
        "scs_cn": 70,
        "weight_precip_short": 0.40, "weight_api": 0.45, "weight_freezing": 0.15,
        "lat": -29.910, "lon": -71.275
    },
    "la_florida": {
        "name": "Sector La Florida / Aeródromo",
        "type": "Urbano / Servicios",
        "elevation_m": 65, "radius_m": 1000,
        "disaster_type": "Anegamiento Vial Urbano",
        "concentration_time_hours": 2.0,
        "recovery_drain_hours": 2.0,
        "scs_cn": 85,
        "weight_precip_short": 0.45, "weight_api": 0.45, "weight_freezing": 0.10,
        "lat": -29.915, "lon": -71.220
    },
    "ruta5_pasos_nivel": {
        "name": "Ruta 5 Norte & Pasos Bajo Nivel (Km 490-500)",
        "type": "Arteria Vial Crítica",
        "elevation_m": 10, "radius_m": 800,
        "disaster_type": "Corte de Ruta 5 e Inundación de Pasos Bajo Nivel",
        "concentration_time_hours": 4.0,
        "recovery_drain_hours": 3.0,
        "scs_cn": 92,
        "weight_precip_short": 0.55, "weight_api": 0.35, "weight_freezing": 0.10,
        "lat": -29.890, "lon": -71.260
    },
    "el_molle": {
        "name": "El Molle & Quebradas",
        "type": "Valle Precordillerano",
        "elevation_m": 450, "radius_m": 1200,
        "disaster_type": "Aluvión y Crecida de Río",
        "concentration_time_hours": 1.2,
        "recovery_drain_hours": 2.5,
        "scs_cn": 85,
        "weight_precip_short": 0.45, "weight_api": 0.35, "weight_freezing": 0.20,
        "lat": -29.978, "lon": -70.923
    },
    "marquesa": {
        "name": "Marquesa & Río Claro",
        "type": "Valle Precordillerano",
        "elevation_m": 500, "radius_m": 1400,
        "disaster_type": "Desborde de Río Claro",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 3.0,
        "scs_cn": 86,
        "weight_precip_short": 0.50, "weight_api": 0.35, "weight_freezing": 0.15,
        "lat": -29.967, "lon": -70.963
    },
    "vicuna_access": {
        "name": "Acceso Vicuña / Ruta 41 Alta",
        "type": "Arteria Vial Precordillera",
        "elevation_m": 600, "radius_m": 1500,
        "disaster_type": "Corte de Ruta por Aluvión",
        "concentration_time_hours": 1.0,
        "recovery_drain_hours": 2.0,
        "scs_cn": 88,
        "weight_precip_short": 0.50, "weight_api": 0.30, "weight_freezing": 0.20,
        "lat": -30.030, "lon": -70.710
    },
    "penuelas": {
        "name": "Sector Peñuelas & Ruta 5 Sur",
        "type": "Urbano Costero",
        "elevation_m": 15, "radius_m": 1200,
        "disaster_type": "Anegamiento Vial",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 2.0,
        "scs_cn": 89,
        "weight_precip_short": 0.50, "weight_api": 0.40, "weight_freezing": 0.10,
        "lat": -29.950, "lon": -71.270
    },
    "guanaqueros_corridor": {
        "name": "Corredor Guanaqueros",
        "type": "Costero Sur",
        "elevation_m": 25, "radius_m": 1500,
        "disaster_type": "Corte de Ruta y Deslizamiento",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 3.0,
        "scs_cn": 82,
        "weight_precip_short": 0.45, "weight_api": 0.40, "weight_freezing": 0.15,
        "lat": -30.198, "lon": -71.423
    },
    "tongoy_access": {
        "name": "Acceso Tongoy / Quebrada Seca",
        "type": "Costero Sur",
        "elevation_m": 10, "radius_m": 1600,
        "disaster_type": "Inundación por Quebrada",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 4.0,
        "scs_cn": 80,
        "weight_precip_short": 0.45, "weight_api": 0.45, "weight_freezing": 0.10,
        "lat": -30.250, "lon": -71.490
    },
    "juan_soldado": {
        "name": "Cerro Juan Soldado & Norte",
        "type": "Cerros Costa Norte",
        "elevation_m": 250, "radius_m": 1400,
        "disaster_type": "Escorrentía Rápida",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 2.0,
        "scs_cn": 85,
        "weight_precip_short": 0.50, "weight_api": 0.35, "weight_freezing": 0.15,
        "lat": -29.680, "lon": -71.280
    },
    "punta_teatinos": {
        "name": "Punta Teatinos & Humedal",
        "type": "Humedal Costero",
        "elevation_m": 5, "radius_m": 1200,
        "disaster_type": "Desborde de Humedal",
        "concentration_time_hours": 4.0,
        "recovery_drain_hours": 5.0,
        "scs_cn": 75,
        "weight_precip_short": 0.35, "weight_api": 0.50, "weight_freezing": 0.15,
        "lat": -29.820, "lon": -71.275
    },
    "el_arrayan": {
        "name": "Quebrada El Arrayán Costero",
        "type": "Quebrada Norte",
        "elevation_m": 60, "radius_m": 1200,
        "disaster_type": "Aluvión de Quebrada",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 2.5,
        "scs_cn": 86,
        "weight_precip_short": 0.50, "weight_api": 0.35, "weight_freezing": 0.15,
        "lat": -29.740, "lon": -71.300
    },
    "andacollo_access": {
        "name": "Ruta D-43 / Acceso Andacollo",
        "type": "Ruta Precordillera",
        "elevation_m": 400, "radius_m": 1500,
        "disaster_type": "Corte de Ruta por Aluvión",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 3.0,
        "scs_cn": 88,
        "weight_precip_short": 0.45, "weight_api": 0.40, "weight_freezing": 0.15,
        "lat": -30.100, "lon": -71.180
    },
    "condoriaco_access": {
        "name": "Acceso Condoriaco / Ruta D-205",
        "type": "Rural Interior",
        "elevation_m": 800, "radius_m": 1600,
        "disaster_type": "Aislamiento por Crecida",
        "concentration_time_hours": 1.0,
        "recovery_drain_hours": 2.0,
        "scs_cn": 87,
        "weight_precip_short": 0.50, "weight_api": 0.30, "weight_freezing": 0.20,
        "lat": -29.690, "lon": -70.950
    },
    "totoralillo": {
        "name": "Totoralillo & Las Tacas",
        "type": "Borde Costero Sur",
        "elevation_m": 15, "radius_m": 1200,
        "disaster_type": "Anegamiento Vial Costero",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 3.0,
        "scs_cn": 82,
        "weight_precip_short": 0.45, "weight_api": 0.45, "weight_freezing": 0.10,
        "lat": -30.060, "lon": -71.320
    },
    "pan_de_azucar": {
        "name": "Pan de Azúcar Sur",
        "type": "Agrícola Periurbano",
        "elevation_m": 100, "radius_m": 1400,
        "disaster_type": "Apozamiento Agrícola",
        "concentration_time_hours": 2.5,
        "recovery_drain_hours": 4.0,
        "scs_cn": 78,
        "weight_precip_short": 0.40, "weight_api": 0.50, "weight_freezing": 0.10,
        "lat": -30.010, "lon": -71.200
    },
    "embalse_puclaro": {
        "name": "Borde Embalse Puclaro",
        "type": "Infraestructura Crítica",
        "elevation_m": 430, "radius_m": 1800,
        "disaster_type": "Crecida de Embalse / Deslizamiento",
        "concentration_time_hours": 1.5,
        "recovery_drain_hours": 6.0,
        "scs_cn": 80,
        "weight_precip_short": 0.30, "weight_api": 0.50, "weight_freezing": 0.20,
        "lat": -30.010, "lon": -70.830
    },
    "herradura_oriente": {
        "name": "La Herradura Oriente / Sindempart",
        "type": "Urbano Residencial Sur",
        "elevation_m": 25, "radius_m": 1100,
        "disaster_type": "Anegamiento de Colectores",
        "concentration_time_hours": 3.5,
        "recovery_drain_hours": 2.0,
        "scs_cn": 90,
        "weight_precip_short": 0.50, "weight_api": 0.40, "weight_freezing": 0.10,
        "lat": -29.980, "lon": -71.350
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


def calculate_scs_direct_runoff(precip_mm: float, cn: float) -> float:
    """Calculates SCS Direct Runoff Q = (P - 0.2S)^2 / (P + 0.8S)"""
    if precip_mm <= 0 or cn <= 0:
        return 0.0
    S = (25400.0 / cn) - 254.0
    ia = 0.2 * S
    if precip_mm <= ia:
        return 0.0
    return float(((precip_mm - ia) ** 2) / (precip_mm + 0.8 * S))


def scan_full_la_serena_grid() -> dict:
    raw_df = fetch_live_nrt_data()
    features_df = generate_hydrological_features(raw_df)
    model, feature_cols = load_jupiter_model()
    current_row = get_current_nrt_row(features_df)
    valid_cols = [col for col in feature_cols if col in current_row.index]
    X_current = pd.DataFrame([[current_row[c] for c in valid_cols]], columns=valid_cols)

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

    forecast_1h = float(current_row.get("precip_forecast_1h", 0.0))
    forecast_3h = float(current_row.get("precip_forecast_3h", 0.0))
    forecast_6h = float(current_row.get("precip_forecast_6h", 0.0))
    forecast_12h = float(current_row.get("precip_forecast_12h", 0.0))
    forecast_24h = float(current_row.get("precip_forecast_24h", 0.0))

    # 5 New Predictive Features (Integrated)
    nowcast_rate = float(current_row.get("nowcast_rain_rate", 0.0))
    geotech_fs = float(current_row.get("geotech_fs", 2.0))
    muskingum_q = float(current_row.get("muskingum_cunge_q", 0.0))
    phys_constraint = float(current_row.get("physics_informed_constraint", 0.0))
    enkf_corr = float(current_row.get("enkf_assimilation_correction", 0.0))

    # Blend with CEAZAMET ground-truth observations in real-time
    _, ceazamet_summary = get_ceazamet_ground_truth_summary()
    if ceazamet_summary.get("ceazamet_available"):
        obs_peak = float(ceazamet_summary.get("peak_precipitation_mm", 0.0))
        obs_avg = float(ceazamet_summary.get("communal_avg_precipitation_mm", 0.0))
        ground_obs = max(obs_peak, obs_avg)
        nowcast_rate = max(nowcast_rate, ground_obs)
        enkf_corr = max(enkf_corr, ground_obs)
        precip_24h = max(precip_24h, ground_obs)
        precip_6h = max(precip_6h, ground_obs)


    precip_signal = np.clip((precip_24h + precip_6h * 2.0) / 15.0, 0.0, 1.0)
    soil_signal = np.clip(api_72h / 15.0, 0.0, 1.0)
    water_presence = max(precip_signal, soil_signal)

    current_dt = pd.to_datetime(current_row["time"])

    scanned_sectors = []
    red_count = 0
    yellow_count = 0

    for key, info in LA_SERENA_SECTOR_GRID.items():
        cn = info.get("scs_cn", 80)
        direct_Q = calculate_scs_direct_runoff(precip_24h, cn)

        freezing_factor = 1.5 if high_freezing == 1 and info["weight_freezing"] > 0.1 else 1.0
        
        base_score = (
            info["weight_precip_short"] * (precip_6h / 20.0) +
            info["weight_api"] * (api_72h / 25.0) +
            0.2 * base_ml_prob +
            0.1 * min(1.0, direct_Q / 10.0) +
            0.1 * min(1.0, forecast_3h / 15.0) +
            0.15 * min(1.0, forecast_6h / 15.0) +
            0.1 * min(1.0, forecast_12h / 20.0) +
            0.05 * min(1.0, nowcast_rate / 10.0) + 
            0.05 * min(1.0, muskingum_q / 50.0) +
            0.05 * min(1.0, enkf_corr / 10.0)
        )
        
        # Physics-informed geotech override
        if geotech_fs < 1.0 and info['type'] in ['Ladera / Faldeo', 'Alta Precordillera', 'Cerros y Quebradas Norte']:
            base_score = max(base_score, 0.85)
        
        # Apply physics-informed constraint penalty if mass conservation fails (e.g., phys_constraint is high)
        if phys_constraint > 10.0:
            base_score += 0.05
        
        score = min(1.0, base_score * water_presence * freezing_factor)

        # -------------------------------------------------------------------------
        # Physical Safety Safeguards (Reglas de Coherencia Física Inviolables)
        # Previenen falsas alarmas de evacuación durante lluvias débiles/moderadas
        # -------------------------------------------------------------------------
        if precip_24h < 10.0 and direct_Q < 1.0 and geotech_fs >= 1.0:
            # Lluvia débil sin escorrentía superficial -> Mantener estrictamente en VERDE (max 25%)
            score = min(score, 0.25)
        elif precip_24h < 25.0 and direct_Q < 5.0 and geotech_fs >= 1.0:
            # Lluvia moderada sin escorrentía crítica -> Mantener máximo en AMARILLA (max 55%)
            score = min(score, 0.55)

        score_pct = round(score * 100.0, 1)

        tc_hours = info["concentration_time_hours"]
        drain_hours = info.get("recovery_drain_hours", 2.0)

        # Dynamic Forecast Peak & Safe Clearance Scanning across Multi-Model Ensemble
        future_df = features_df[features_df["time"] >= current_dt]
        active_rain_df = future_df[future_df["precipitation"] > 0.1]
        
        if not active_rain_df.empty:
            # 1. Punto Máximo de Impacto: Peak forecast hour + Concentration Time Tc
            peak_idx = active_rain_df["precipitation"].idxmax()
            peak_forecast_dt = pd.to_datetime(active_rain_df.loc[peak_idx, "time"])
            eta_impact = peak_forecast_dt + pd.Timedelta(hours=tc_hours)
            eta_impact_formatted = eta_impact.strftime("%d/%m/%Y %H:%M hrs")
            
            # 2. Hora de Paso Seguro (Calma): End of active storm + Drainage Time
            last_rain_dt = pd.to_datetime(active_rain_df["time"].iloc[-1])
            eta_safe_return = last_rain_dt + pd.Timedelta(hours=drain_hours)
            eta_safe_formatted = eta_safe_return.strftime("%d/%m/%Y %H:%M hrs")
        elif score > 0.3:
            eta_impact = current_dt + pd.Timedelta(hours=tc_hours)
            eta_impact_formatted = eta_impact.strftime("%d/%m/%Y %H:%M hrs")
            eta_safe_return = eta_impact + pd.Timedelta(hours=drain_hours + 2.0)
            eta_safe_formatted = eta_safe_return.strftime("%d/%m/%Y %H:%M hrs")
        else:
            eta_impact_formatted = "Sin Lluvia Prevista"
            eta_safe_formatted = "Condición Estable (Transitable)"

        if score >= 0.7:
            semaforo = "ALERTA ROJA"
            transitability = f"TRANSITO RESTRICTORIO (Hora de Paso Seguro (Calma): {eta_safe_formatted})"
            red_count += 1
        elif score >= 0.4:
            semaforo = "ALERTA AMARILLA"
            transitability = f"PRECAUCIÓN VIAL (Hora de Paso Seguro (Calma): {eta_safe_formatted})"
            yellow_count += 1
        else:
            semaforo = "VERDE ESTABLE"
            transitability = "TRANSITABLE (Condición Normal)"

        scanned_sectors.append({
            "key": key,
            "name": info["name"],
            "type": info["type"],
            "elevation_m": info["elevation_m"],
            "radius_m": info["radius_m"],
            "disaster_type": info["disaster_type"],
            "concentration_time_hours": tc_hours,
            "recovery_drain_hours": drain_hours,
            "eta_impact": eta_impact_formatted,
            "eta_safe_return": eta_safe_formatted,
            "transitability_status": transitability,
            "scs_curve_number": cn,
            "agua_acumulada_superficie": round(direct_Q, 2),
            "forecast_1h": round(forecast_1h, 1),
            "forecast_3h": round(forecast_3h, 1),
            "forecast_6h": round(forecast_6h, 1),
            "forecast_12h": round(forecast_12h, 1),
            "forecast_24h": round(forecast_24h, 1),
"score_pct": score_pct,
            "geotech_fs": round(geotech_fs, 2),
            "nowcast_rain_rate": round(nowcast_rate, 2),
            "muskingum_q": round(muskingum_q, 2),
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

    _, ceazamet_summary = get_ceazamet_ground_truth_summary()

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
        "ceazamet_telemetry": ceazamet_summary,
        "sectors": scanned_sectors
    }


if __name__ == "__main__":
    scan = scan_full_la_serena_grid()
    print(f"Timestamp: {scan['timestamp']}")
    print(f"Commune Status: {scan['commune_status']}")
    print(f"Total Sectors: {scan['total_sectors_scanned']}")
    print("\nTop 3 Risk Sectors:")
    for s in scan['sectors'][:3]:
        print(f" - {s['name']}: {s['semaforo']} ({s['score_pct']}%) | Llegada del Pico: {s['eta_impact']} | Hora de Paso Seguro (Calma): {s['eta_safe_return']}")
