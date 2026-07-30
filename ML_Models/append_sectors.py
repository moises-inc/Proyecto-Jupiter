import re

content = open("/mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/ML_Models/src/inference/spatial_scanner.py", "r").read()

new_sectors = []
for i in range(1, 16):
    new_sectors.append(f"""    "sector_dummy_{i}": {{
        "name": "Sector Dummy {i}",
        "type": "Urbano / Servicios",
        "elevation_m": 50, "radius_m": 1000,
        "disaster_type": "Anegamiento Vial Urbano",
        "concentration_time_hours": 3.0,
        "recovery_drain_hours": 2.0,
        "scs_cn": 85,
        "weight_precip_short": 0.45, "weight_api": 0.45, "weight_freezing": 0.10,
        "lat": -29.900, "lon": -71.250
    }}""")

new_sectors_str = ",\n".join(new_sectors) + "\n}\n\n\ndef get_current_nrt_row(df: pd.DataFrame) -> pd.Series:"

content = content.replace("}\n\n\ndef get_current_nrt_row(df: pd.DataFrame) -> pd.Series:", ",\n" + new_sectors_str)

with open("/mnt/9b846436-0407-4e80-b8af-5417ffbdee8e/ObsidianVault/10_Projects/Proyecto_Centinela/ML_Models/src/inference/spatial_scanner.py", "w") as f:
    f.write(content)
