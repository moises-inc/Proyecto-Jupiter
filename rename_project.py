import os

files_to_modify = [
    "Dashboard/static/index_realtime.html",
    "Dashboard/static/demo.html",
    "Dashboard/static/js/realtime.js",
    "Dashboard/static/js/demo.js",
    "Dashboard/server.py",
    "ML_Models/src/inference/spatial_scanner.py",
    "ML_Models/src/inference/live_inference.py",
    "ML_Models/src/models/train_flood_predictor.py",
    "ML_Models/src/models/stress_test_model.py",
    "ML_Models/tests/test_pipeline.py",
    "ML_Models/tests/test_sector_precision.py"
]

replacements = [
    ("PROYECTO CENTINELA", "PROYECTO JÚPITER"),
    ("Proyecto Centinela", "Proyecto Júpiter"),
    ("Centinela", "Júpiter"),
    ("centinela", "jupiter"),
    ("CENTINELA", "JÚPITER"),
    ("Ejecucción", "Ejecución"),
    ("load_centinela_model", "load_jupiter_model"),
    ("centinela_sat_v1.joblib", "jupiter_sat_v1.joblib")
]

for filepath in files_to_modify:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We need to be careful with "centinela" -> "jupiter" because of "centinela_sat_v1".
        # Let's apply specific replacements first to avoid issues.
        content = content.replace("load_centinela_model", "load_jupiter_model")
        content = content.replace("centinela_sat_v1.joblib", "jupiter_sat_v1.joblib")
        content = content.replace("PROYECTO CENTINELA", "PROYECTO JÚPITER")
        content = content.replace("Proyecto Centinela", "Proyecto Júpiter")
        content = content.replace("Ejecucción", "Ejecución")
        
        # Then we can do the general ones if there are more
        content = content.replace("Centinela", "Júpiter")
        content = content.replace("centinela", "jupiter")
        content = content.replace("CENTINELA", "JÚPITER")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Modified {filepath}")
    else:
        print(f"File not found: {filepath}")

