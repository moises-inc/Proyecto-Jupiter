import re

content = open("/mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/ML_Models/src/inference/spatial_scanner.py", "r").read()

missing_sector = """    "ruta5_pasos_nivel": {
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
"""

content = content.replace('"sector_dummy_1": {', missing_sector + '    "sector_dummy_1": {')

with open("/mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/ML_Models/src/inference/spatial_scanner.py", "w") as f:
    f.write(content)
