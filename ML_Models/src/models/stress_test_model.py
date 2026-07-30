"""
Proyecto Centinela - Advanced Model Stress Testing Module
Performs sensitivity analysis (What-If scenarios), fault tolerance, and performance profiling.
"""

import time
import pandas as pd
import numpy as np

from src.ingesters.ingest_sat_data import generate_offline_fallback_data
from src.features.feature_engineering import generate_hydrological_features, FEATURE_COLUMNS
from src.inference.live_inference import load_centinela_model, evaluate_sector_tactical_risks


def run_sensitivity_analysis():
    """
    Performs 'What-If' sensitivity analysis across varying rainfall rates and freezing levels.
    """
    print("\n" + "=" * 65)
    print(" 🧪 PRUEBA 1: ANÁLISIS DE SENSIBILIDAD (ESCENARIOS 'WHAT-IF')")
    print("=" * 65)
    print(" Evaluando respuesta del modelo ante incrementos de lluvia e Isoterma Cero:")
    print("-" * 65)
    print(f"{'Lluvia 24h (mm)':<16} | {'Isoterma (m.n.m)':<16} | {'Riesgo ML %':<12} | {'Semáforo General':<20}")
    print("-" * 65)

    base_df = generate_offline_fallback_data("2026-07-20", "2026-07-21")
    feat_df = generate_hydrological_features(base_df)
    model, cols = load_centinela_model()

    base_row = feat_df.iloc[-1].copy()

    # Test rain scenarios from 0mm to 100mm and low/high freezing level
    test_scenarios = [
        (0.0, 2200.0),
        (15.0, 2500.0),
        (30.0, 2800.0),
        (50.0, 3200.0),
        (80.0, 3600.0),
        (120.0, 4000.0),
    ]

    for rain, freezing in test_scenarios:
        test_row = pd.Series(0.0, index=cols)
        test_row["precip_accum_24h"] = rain
        test_row["precip_accum_6h"] = rain * 0.6
        test_row["api_72h"] = rain * 0.5
        test_row["freezing_level_scaled"] = freezing / 1000.0
        test_row["high_freezing_level_flag"] = 1 if freezing > 3000.0 else 0

        X = pd.DataFrame([test_row[cols]])
        prob = float(model.predict_proba(X)[0][1]) if hasattr(model, "predict_proba") and len(model.classes_) > 1 else 0.0
        
        # Water presence gating factor
        precip_signal = np.clip((rain + (rain * 0.6) * 2.0) / 15.0, 0.0, 1.0)
        soil_signal = np.clip((rain * 0.5) / 15.0, 0.0, 1.0)
        water_presence = max(precip_signal, soil_signal)

        freezing_factor = 1.0 + 0.5 * test_row["high_freezing_level_flag"]
        norm_accum = np.clip(rain / 80.0, 0.0, 1.0)
        norm_api = np.clip((rain * 0.5) / 60.0, 0.0, 1.0)
        base_risk = (0.6 * norm_accum + 0.4 * norm_api)
        
        risk = min(1.0, max(prob, base_risk) * water_presence * freezing_factor)

        tactic = evaluate_sector_tactical_risks(test_row, risk)

        print(f"{rain:<16.1f} | {freezing:<16.0f} | {risk*100:<12.1f}% | {tactic['general_semaforo']:<20}")

    print("=" * 65 + "\n")


def run_fault_tolerance_test():
    """
    Tests how the model handles corrupted data (NaNs, extreme outliers).
    """
    print("\n" + "=" * 65)
    print(" 🛡️ PRUEBA 2: TOLERANCIA A CORRUPCIÓN DE DATOS Y FALLOS DE RED")
    print("=" * 65)

    base_df = generate_offline_fallback_data("2026-07-20", "2026-07-21")
    
    # Inject NaNs and corrupted spikes
    base_df.loc[0, "precipitation"] = np.nan
    base_df.loc[1, "freezing_level_height"] = 99999.0 # Extreme outlier spike

    try:
        feat_df = generate_hydrological_features(base_df)
        model, cols = load_centinela_model()
        X = pd.DataFrame([feat_df.iloc[-1][cols]])
        pred = model.predict(X)
        print(" SUCCESS: El pipeline procesó datos corruptos/NaNs sin colapsar.")
        print(f" Inferencia procesada en limpio con etiqueta de salida: {pred[0]}")
    except Exception as e:
        print(f" ERROR: El pipeline falló ante datos corruptos: {e}")
    
    print("=" * 65 + "\n")


def run_latency_profiling():
    """
    Profiles inference latency across 100 consecutive predictions.
    """
    print("\n" + "=" * 65)
    print(" ⚡ PRUEBA 3: PROFILING DE VELOCIDAD Y LATENCIA DE INFERENCIA")
    print("=" * 65)

    base_df = generate_offline_fallback_data("2026-07-20", "2026-07-21")
    feat_df = generate_hydrological_features(base_df)
    model, cols = load_centinela_model()
    X = pd.DataFrame([feat_df.iloc[-1][cols]])

    start_time = time.time()
    iterations = 100
    for _ in range(iterations):
        _ = model.predict(X)
    elapsed = time.time() - start_time

    avg_ms = (elapsed / iterations) * 1000.0
    print(f" Total tiempo para {iterations} inferencias: {elapsed:.4f} segundos")
    print(f" Tiempo promedio por inferencia: {avg_ms:.2f} milisegundos")
    print(f" Veredicto: {'APROBADO (< 10 ms)' if avg_ms < 10.0 else 'ADVERTENCIA (> 10 ms)'}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run_sensitivity_analysis()
    run_fault_tolerance_test()
    run_latency_profiling()
