import re

with open("src/inference/spatial_scanner.py", "r") as f:
    content = f.read()

# Modify base_score to use forecast_6h and forecast_12h
new_base_score = """
        base_score = (
            info["weight_precip_short"] * (precip_6h / 20.0) +
            info["weight_api"] * (api_72h / 25.0) +
            0.2 * base_ml_prob +
            0.1 * min(1.0, direct_Q / 10.0) +
            0.1 * min(1.0, forecast_3h / 15.0) +
            0.15 * min(1.0, forecast_6h / 15.0) +
            0.1 * min(1.0, forecast_12h / 20.0)
        )"""

# Regex replace the base_score block
content = re.sub(
    r'base_score = \([\s\S]*?forecast_3h / 15\.0\)\n\s*\)',
    new_base_score.strip(),
    content
)

with open("src/inference/spatial_scanner.py", "w") as f:
    f.write(content)

