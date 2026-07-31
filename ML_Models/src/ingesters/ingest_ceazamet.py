"""
Proyecto Júpiter - CEAZAMET Ground Station Telemetry Ingester
Retrieves real-time meteorological observations from the CEAZAMET network
(Red de Estaciones de Terreno CEAZAMET) for EnKF assimilation and ML model
risk recalibration in La Serena / Valle del Elqui.
"""

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional, Tuple


CEAZAMET_BASE_URL = "https://www.ceazamet.cl/modulos/pop_estacion_info.php"

CEAZAMET_STATIONS = {
    "LSC": {
        "name": "La Serena [CEAZA]",
        "lat": -29.915, "lon": -71.242, "elevation_m": 90
    },
    "CGR": {
        "name": "La Serena [Cerro Grande]",
        "lat": -29.938, "lon": -71.224, "elevation_m": 513
    },
    "5": {
        "name": "La Serena [El Romeral]",
        "lat": -29.754, "lon": -71.257, "elevation_m": 162
    },
    "3": {
        "name": "Pan de Azúcar",
        "lat": -30.075, "lon": -71.239, "elevation_m": 135
    },
    "9": {
        "name": "Gabriela Mistral",
        "lat": -29.979, "lon": -71.080, "elevation_m": 198
    },
    "6": {
        "name": "Vicuña",
        "lat": -30.038, "lon": -70.697, "elevation_m": 634
    },
    "4": {
        "name": "Coquimbo [El Panul]",
        "lat": -29.999, "lon": -71.399, "elevation_m": 122
    }
}


def parse_ceazamet_html(html_content: str, e_cod: str) -> Dict:
    soup = BeautifulSoup(html_content, "html.parser")
    result = {
        "station_id": e_cod,
        "station_name": CEAZAMET_STATIONS.get(e_cod, {}).get("name", f"Station_{e_cod}"),
        "precipitation_mm": None,
        "temperature_c": None,
        "wind_speed_kmh": None,
        "wind_direction": None,
        "relative_humidity_pct": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).lower()
                value_cell = cells[1].get_text(strip=True)
                value = _parse_numeric(value_cell)
                if "precipitaci" in label or "lluvia" in label:
                    if value is not None:
                        result["precipitation_mm"] = value
                elif "temperatur" in label:
                    if value is not None:
                        result["temperature_c"] = value
                elif "humeda" in label:
                    if value is not None:
                        result["relative_humidity_pct"] = value
                elif "velocidad del viento" in label or "viento" in label:
                    if value is not None:
                        result["wind_speed_kmh"] = value
                elif "direcci" in label:
                    dir_text = value_cell.strip()
                    result["wind_direction"] = dir_text if dir_text else None
    return result


def _parse_numeric(text: str) -> Optional[float]:
    cleaned = text.strip().replace(",", ".")
    if not cleaned:
        return None
    parts = cleaned.split()
    for part in parts:
        try:
            return float(part)
        except ValueError:
            continue
    return None


def fetch_ceazamet_station_data(e_cod: str) -> Dict:
    station_info = CEAZAMET_STATIONS.get(e_cod)
    if station_info is None:
        return {
            "station_id": e_cod,
            "ceazamet_available": False,
            "error": f"Unknown station code: {e_cod}"
        }
    try:
        response = requests.get(
            CEAZAMET_BASE_URL,
            params={"e_cod": e_cod},
            timeout=10
        )
        response.raise_for_status()
        parsed = parse_ceazamet_html(response.text, e_cod)
        parsed["ceazamet_available"] = True
        parsed["lat"] = station_info["lat"]
        parsed["lon"] = station_info["lon"]
        parsed["elevation_m"] = station_info["elevation_m"]
        return parsed
    except requests.exceptions.Timeout:
        return {
            "station_id": e_cod,
            "ceazamet_available": False,
            "error": "Timeout connecting to CEAZAMET server"
        }
    except requests.exceptions.RequestException as e:
        return {
            "station_id": e_cod,
            "ceazamet_available": False,
            "error": f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            "station_id": e_cod,
            "ceazamet_available": False,
            "error": f"Parse error: {str(e)}"
        }


def fetch_all_la_serena_stations() -> List[Dict]:
    results = []
    for e_cod in CEAZAMET_STATIONS:
        data = fetch_ceazamet_station_data(e_cod)
        results.append(data)
    return results


def get_ceazamet_ground_truth_summary() -> Tuple[pd.DataFrame, Dict]:
    stations_data = fetch_all_la_serena_stations()
    available = [s for s in stations_data if s.get("ceazamet_available") and s.get("precipitation_mm") is not None]

    precip_values = [s["precipitation_mm"] for s in available]
    temp_values = [s["temperature_c"] for s in available if s.get("temperature_c") is not None]

    df = pd.DataFrame(available) if available else pd.DataFrame()

    summary = {
        "ceazamet_available": len(available) > 0,
        "stations_online": len(available),
        "stations_total": len(CEAZAMET_STATIONS),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "communal_avg_precipitation_mm": round(float(np.mean(precip_values)), 1) if precip_values else 0.0,
        "peak_precipitation_mm": round(float(np.max(precip_values)), 1) if precip_values else 0.0,
        "peak_station": available[precip_values.index(max(precip_values))]["station_name"] if precip_values else None,
        "avg_temperature_c": round(float(np.mean(temp_values)), 1) if temp_values else 0.0,
        "stations": available
    }

    return df, summary
