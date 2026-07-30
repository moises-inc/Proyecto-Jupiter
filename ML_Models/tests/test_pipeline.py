"""
Proyecto Júpiter - Pipeline Unit and Integration Tests
Tests data ingestion, feature engineering, model training, and live inference.
"""

import os
import pytest
import pandas as pd
import numpy as np

from src.ingesters.ingest_sat_data import fetch_open_meteo_data, generate_offline_fallback_data
from src.features.feature_engineering import (
    generate_hydrological_features,
    compute_antecedent_precipitation_index,
    FEATURE_COLUMNS
)
from src.models.train_flood_predictor import train_and_evaluate_model, MODEL_DIR
from src.inference.live_inference import run_live_inference, load_jupiter_model


def test_data_ingestion():
    df = generate_offline_fallback_data("2026-07-14", "2026-07-21")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "precipitation" in df.columns
    assert "freezing_level_height" in df.columns


def test_feature_engineering():
    raw_df = generate_offline_fallback_data("2026-07-14", "2026-07-21")
    features_df = generate_hydrological_features(raw_df)

    assert "api_72h" in features_df.columns
    assert "precip_accum_24h" in features_df.columns
    assert "risk_score" in features_df.columns
    assert "overflow_target" in features_df.columns

    for col in FEATURE_COLUMNS:
        assert col in features_df.columns
        assert not features_df[col].isna().any(), f"NaN values detected in feature column: {col}"


def test_antecedent_precipitation_index():
    precip = pd.Series([0.0, 10.0, 5.0, 0.0, 0.0])
    api = compute_antecedent_precipitation_index(precip, decay_factor=0.85)

    assert api[0] == 0.0
    assert api[1] == 10.0
    assert api[2] == 5.0 + 0.85 * 10.0  # 13.5
    assert api[3] == 0.0 + 0.85 * 13.5  # 11.475


def test_model_training_and_serialization():
    raw_df = generate_offline_fallback_data("2025-05-01", "2026-07-25")
    features_df = generate_hydrological_features(raw_df)

    test_model_filename = "test_jupiter_model.joblib"
    artifact = train_and_evaluate_model(features_df, model_filename=test_model_filename)

    test_model_path = os.path.join(MODEL_DIR, test_model_filename)
    assert os.path.exists(test_model_path)
    assert "model" in artifact
    assert artifact["metrics"]["accuracy"] > 0.5


def test_live_inference_end_to_end():
    # Ensure default model is trained
    raw_df = generate_offline_fallback_data("2025-05-01", "2026-07-25")
    features_df = generate_hydrological_features(raw_df)
    train_and_evaluate_model(features_df, model_filename="jupiter_sat_v1.joblib")

    bulletin = run_live_inference()

    assert "timestamp" in bulletin
    assert "telemetry_metrics" in bulletin
    assert "tactic" in bulletin
    assert "general_semaforo" in bulletin["tactic"]
    assert "pueblo_islon" in bulletin["tactic"]["sectors"]
    assert "las_companias" in bulletin["tactic"]["sectors"]
    assert "la_serena_urbana" in bulletin["tactic"]["sectors"]
