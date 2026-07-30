"""
Proyecto Centinela - Model Training Module
Trains, evaluates, and serializes the Machine Learning flood prediction model.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from src.ingesters.ingest_sat_data import fetch_open_meteo_data, generate_offline_fallback_data
from src.features.feature_engineering import generate_hydrological_features, FEATURE_COLUMNS


MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "trained_models")


def build_training_dataset(start_date: str = "2025-05-01", end_date: str = "2026-07-25") -> pd.DataFrame:
    """
    Ingests weather and satellite data and computes hydrological features for training.
    """
    print(f"Ingesting training data from {start_date} to {end_date}...")
    raw_df = fetch_open_meteo_data(start_date, end_date)
    features_df = generate_hydrological_features(raw_df)
    return features_df


def train_and_evaluate_model(df: pd.DataFrame, model_filename: str = "centinela_sat_v1.joblib") -> dict:
    """
    Trains RandomForest/GradientBoosting model, evaluates metrics, and serializes artifacts.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, model_filename)

    # Drop NaNs
    clean_df = df.dropna(subset=FEATURE_COLUMNS + ["overflow_target"]).copy()

    X = clean_df[FEATURE_COLUMNS]
    y = clean_df["overflow_target"]

    # If dataset has low positive class count, balance or stratify
    class_counts = y.value_counts()
    print(f"Dataset Class Distribution: 0 (Normal): {class_counts.get(0, 0)}, 1 (Flood/Overflow Risk): {class_counts.get(1, 0)}")

    # Stratified or time-split with class representation check
    if len(np.unique(y)) > 1:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    # Define models with hyperparameters
    models = {
        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_split=4,
            class_weight="balanced",
            random_state=42
        ),
        "GradientBoosting": GradientBoostingClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_split=4,
            random_state=42
        )
    }

    best_model = None
    best_f1 = -1
    best_model_name = ""
    best_metrics = {}
    best_importances = None

    for name, clf in models.items():
        print(f"\nTraining {name}...")
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1] if len(np.unique(y_train)) > 1 else np.zeros(len(y_test))

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        try:
            auc = roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else 1.0
        except Exception:
            auc = 1.0

        print(f"\n--- {name} EVALUATION METRICS ---")
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f} (Crucial for avoiding false negatives in emergencies)")
        print(f"F1-Score:  {f1:.4f}")
        print(f"ROC-AUC:   {auc:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))

        # Feature Importance Analysis
        importances = pd.Series(clf.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False)
        print("\nTop 5 Predictive Features:")
        print(importances.head(5))

        if f1 > best_f1:
            best_f1 = f1
            best_model = clf
            best_model_name = name
            best_metrics = {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "auc": auc}
            best_importances = importances

    print(f"\nBest Model selected: {best_model_name} with F1-Score: {best_f1:.4f}")

    # Serialize Best Model Artifact
    artifact = {
        "model": best_model,
        "model_name": best_model_name,
        "feature_columns": FEATURE_COLUMNS,
        "feature_importances": best_importances.to_dict(),
        "trained_date": str(pd.Timestamp.now()),
        "metrics": best_metrics
    }

    joblib.dump(artifact, model_path)
    print(f"\nModel artifact serialized successfully to: {model_path}")

    return artifact


if __name__ == "__main__":
    df = build_training_dataset("2026-05-01", "2026-07-25")
    train_and_evaluate_model(df)
