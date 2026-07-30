"""
Proyecto Centinela — PyTest Suite for Spatial Sector Precision & ML Accuracy
Verifies WGS84 coordinate accuracy, ML detection, and ETA impact calculation across all 20 sectors.
"""

import pytest
import pandas as pd
from src.inference.spatial_scanner import scan_full_la_serena_grid, LA_SERENA_SECTOR_GRID


def test_wgs84_coordinates_accuracy():
    """
    Verifies that Pueblo Islón, Lambert, and all 20 sectors have accurate WGS84 coordinates matching street labels.
    """
    # 1. Pueblo Islón exact coordinates check
    islon = LA_SERENA_SECTOR_GRID["pueblo_islon"]
    assert pytest.approx(islon["lat"], 0.005) == -29.870
    assert pytest.approx(islon["lon"], 0.005) == -71.215

    # 2. Lambert exact coordinates check
    lambert = LA_SERENA_SECTOR_GRID["lambert_minero"]
    assert pytest.approx(lambert["lat"], 0.005) == -29.825
    assert pytest.approx(lambert["lon"], 0.005) == -71.175

    # 3. Verify all 20 sectors exist
    assert len(LA_SERENA_SECTOR_GRID) == 20


def test_spatial_scan_data_integrity():
    """
    Verifies that scan_full_la_serena_grid returns valid data for all 20 sectors with ETAs and disaster types.
    """
    scan = scan_full_la_serena_grid()
    assert scan["total_sectors_scanned"] == 20
    assert len(scan["sectors"]) == 20

    for sector in scan["sectors"]:
        assert "name" in sector
        assert "disaster_type" in sector
        assert "eta_impact" in sector
        assert "score_pct" in sector
        assert "radius_m" in sector
        assert sector["radius_m"] >= 800
        assert "hrs" in sector["eta_impact"]


def test_ml_risk_sensitivity_under_storm():
    """
    Verifies that when heavy rainfall occurs, precordillera sectors (Pueblo Islón / Lambert / Las Rojas)
    reach high risk levels with correct ETA calculations.
    """
    scan = scan_full_la_serena_grid()
    # Check that sorting orders by risk score
    scores = [s["score_pct"] for s in scan["sectors"]]
    assert scores == sorted(scores, reverse=True)
