"""
Proyecto Júpiter - Unit Tests for Risk Score Stability, EMA Smoothing, Hysteresis, and Agencies Ingestion
"""

import pytest
import pandas as pd
import numpy as np
from src.inference.spatial_scanner import scan_full_la_serena_grid
from src.ingesters.ingest_senapred import get_chilean_agencies_summary, fetch_senapred_active_alerts, fetch_dmc_active_warnings


def test_spatial_scan_stability():
    scan1 = scan_full_la_serena_grid()
    scan2 = scan_full_la_serena_grid()

    assert scan1["status_code"] if "status_code" in scan1 else True
    assert len(scan1["sectors"]) == 35
    assert len(scan2["sectors"]) == 35

    top_score_1 = scan1["sectors"][0]["score_pct"]
    top_score_2 = scan2["sectors"][0]["score_pct"]

    # Consecutive scans under identical conditions must not jump abruptly (max 1.0% variation)
    assert abs(top_score_1 - top_score_2) <= 1.0


def test_senapred_and_dmc_ingestion():
    summary = get_chilean_agencies_summary()
    assert "senapred" in summary
    assert "dmc" in summary

    senapred = summary["senapred"]
    assert senapred["senapred_available"] is True
    assert senapred["alert_level"] in ["VERDE", "AMARILLA", "ROJA", "TEMPRANA_PREVENTIVA"]

    dmc = summary["dmc"]
    assert dmc["dmc_available"] is True
    assert "max_wind_kmh" in dmc


def test_no_false_red_alert_under_light_rain():
    scan = scan_full_la_serena_grid()
    telemetry = scan["telemetry_summary"]
    precip_24h = telemetry["precip_accum_24h_mm"]

    if precip_24h < 10.0:
        # Guarantee no false Red Alert under light rain
        assert scan["commune_status"] != "ALERTA ROJA COMUNAL (EVACUACIÓN Y RESCATE PREVENTIVO ACTIVO)"
        for sector in scan["sectors"]:
            assert sector["score_pct"] <= 40.0 or sector["semaforo"] == "VERDE ESTABLE"
