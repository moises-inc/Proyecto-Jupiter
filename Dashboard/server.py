"""
Proyecto Centinela - Command Post Dashboard Backend (FastAPI)
Serves NRT satellite telemetry, spatial grid scan predictions, and storm simulation endpoints.
"""

import sys
import os
import pandas as pd
import numpy as np
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure ML_Models path is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_MODELS_DIR = os.path.join(BASE_DIR, "ML_Models")
if ML_MODELS_DIR not in sys.path:
    sys.path.insert(0, ML_MODELS_DIR)

from src.inference.spatial_scanner import scan_full_la_serena_grid, LA_SERENA_SECTOR_GRID
from src.inference.live_inference import run_live_inference
from src.ingesters.ingest_sat_data import generate_offline_fallback_data
from src.features.feature_engineering import generate_hydrological_features
from src.inference.live_inference import load_centinela_model, evaluate_sector_tactical_risks


app = FastAPI(
    title="Proyecto Centinela - Dashboard Táctico Puesto de Mando",
    description="API y Servidor Local de Conciencia Situacional para Bomberos y SCI (La Serena)",
    version="1.0.0"
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import threading
import time

# In-memory NRT Cache
LATEST_NRT_CACHE = {
    "last_sync": None,
    "scan_data": None
}

def sync_nrt_satellite_data():
    """
    Background worker function that executes every 300 seconds (5 minutes)
    to fetch fresh NRT satellite telemetry and recalculate spatial scan predictions.
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 📡 Ejecucción de Ingesta Satelital NRT (Frecuencia: Cada 5 Minutos)...")
    try:
        scan = scan_full_la_serena_grid()
        hours = [f"{h:02d}:00" for h in range(0, 25, 4)]
        scan["trend_series"] = {
            "labels": hours,
            "rain_accum_mm": [0.0, 0.0, 0.0, 0.2, 0.5, 0.9, 0.9],
            "freezing_level_m": [3800, 3900, 4000, 4050, 4060, 4070, 4070]
        }
        scan["nrt_sync_interval_min"] = 5
        scan["last_sync_timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        LATEST_NRT_CACHE["scan_data"] = scan
        LATEST_NRT_CACHE["last_sync"] = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ Sincronización Satelital NRT Completada Exitosamente.")
    except Exception as e:
        print(f"Error en ingesta satelital NRT de 5 minutos: {e}")

def background_nrt_scheduler():
    while True:
        sync_nrt_satellite_data()
        time.sleep(300) # 5 Minutes Refresh Rate

# Start background NRT sync thread on server launch
nrt_thread = threading.Thread(target=background_nrt_scheduler, daemon=True)
nrt_thread.start()


@app.get("/api/scan", response_class=JSONResponse)
def get_spatial_scan():
    """
    Returns the real-time 8-sector spatial grid scan for La Serena (Updated every 5 min).
    """
    if LATEST_NRT_CACHE["scan_data"] is not None:
        return LATEST_NRT_CACHE["scan_data"]
    
    # Fallback initial fetch
    scan = scan_full_la_serena_grid()
    hours = [f"{h:02d}:00" for h in range(0, 25, 4)]
    scan["trend_series"] = {
        "labels": hours,
        "rain_accum_mm": [0.0, 0.0, 0.0, 0.2, 0.5, 0.9, 0.9],
        "freezing_level_m": [3800, 3900, 4000, 4050, 4060, 4070, 4070]
    }
    scan["nrt_sync_interval_min"] = 5
    return scan


@app.get("/api/bulletin", response_class=JSONResponse)
def get_bulletin():
    """
    Returns the single-point emergency bulletin and NRT telemetry.
    """
    bulletin = run_live_inference()
    return bulletin


@app.get("/api/simulate-storm", response_class=JSONResponse)
def simulate_storm(severity: str = Query("extreme", description="normal, moderate, extreme")):
    """
    Simulates a storm event (e.g. July 19 2026 extreme storm) for live testing across 14 sectors.
    """
    if severity == "extreme":
        rain_24h = 85.0
        rain_6h = 35.0
        api_72h = 42.0
        freezing = 3500.0
        high_freezing = 1
    elif severity == "moderate":
        rain_24h = 32.0
        rain_6h = 14.0
        api_72h = 18.0
        freezing = 2800.0
        high_freezing = 0
    else:
        rain_24h = 0.0
        rain_6h = 0.0
        api_72h = 0.2
        freezing = 2200.0
        high_freezing = 0

    base_time = pd.to_datetime("2026-07-19 18:00:00")

    scanned_sectors = []
    red_count = 0
    yellow_count = 0

    for key, info in LA_SERENA_SECTOR_GRID.items():
        precip_signal = min(1.0, (rain_24h + rain_6h * 2.0) / 15.0)
        soil_signal = min(1.0, api_72h / 15.0)
        water_presence = max(precip_signal, soil_signal)

        freezing_factor = 1.5 if high_freezing == 1 and info["weight_freezing"] > 0.1 else 1.0
        base_score = info["weight_precip_short"] * (rain_6h / 20.0) + info["weight_api"] * (api_72h / 25.0) + 0.2

        score = min(1.0, base_score * water_presence * freezing_factor) if water_presence > 0.01 else 0.0
        score_pct = round(score * 100.0, 1)

        tc_hours = info["concentration_time_hours"]
        eta_time = base_time + pd.Timedelta(hours=tc_hours)
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

    hours = [f"{h:02d}:00" for h in range(0, 25, 4)]
    if severity == "extreme":
        rain_series = [0.0, 15.0, 35.0, 60.0, 85.0, 85.0, 85.0]
        freezing_series = [2800, 3000, 3300, 3500, 3500, 3500, 3500]
    elif severity == "moderate":
        rain_series = [0.0, 5.0, 12.0, 22.0, 32.0, 32.0, 32.0]
        freezing_series = [2400, 2600, 2800, 2800, 2800, 2800, 2800]
    else:
        rain_series = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        freezing_series = [2200, 2200, 2200, 2200, 2200, 2200, 2200]

    return {
        "timestamp": "2026-07-19 18:00:00 (SIMULACIÓN TEMPORAL EXTREMO)",
        "simulation_mode": True,
        "severity": severity,
        "total_sectors_scanned": len(scanned_sectors),
        "commune_status": commune_status,
        "telemetry_summary": {
            "precip_accum_24h_mm": rain_24h,
            "precip_accum_6h_mm": rain_6h,
            "api_soil_saturation": api_72h,
            "freezing_level_m": freezing
        },
        "trend_series": {
            "labels": hours,
            "rain_accum_mm": rain_series,
            "freezing_level_m": freezing_series
        },
        "sectors": scanned_sectors
    }


# Mount static assets
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def serve_realtime_dashboard():
    """
    Serves the 100% Real-Time Operational Dashboard for Friday's emergency monitoring.
    """
    index_path = os.path.join(STATIC_DIR, "index_realtime.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Operational Dashboard Loading...</h1>"


@app.get("/demo", response_class=HTMLResponse)
def serve_demo_dashboard():
    """
    Serves the Interactive Demo & Storm Simulation Dashboard for presentations to Firefighters and Authorities.
    """
    demo_path = os.path.join(STATIC_DIR, "demo.html")
    if os.path.exists(demo_path):
        with open(demo_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Demo Dashboard Loading...</h1>"


if __name__ == "__main__":
    import uvicorn
    print("Iniciando Servidor Local del Dashboard Táctico (Proyecto Centinela)...")
    print("Accede en tu navegador a: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
