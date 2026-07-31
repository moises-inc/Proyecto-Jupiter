import pytest
import math
from src.features.nowcasting_engine import NowcastingEngine

def test_dbz_to_rain_rate():
    engine = NowcastingEngine()
    # For dBZ = 40, Z_linear = 10000
    # R = (10000/200)^(1/1.6) = 50^(0.625) approx 11.53
    dbz = 40
    rain_rate = engine.dbz_to_rain_rate(dbz)
    assert math.isclose(rain_rate, 11.53, rel_tol=1e-2)

def test_extrapolate_ir_temperature():
    engine = NowcastingEngine()
    current_temp = -20.0
    temp_trend = -0.5 # cooling 0.5 degrees per minute
    forecasts = engine.extrapolate_ir_temperature(current_temp, temp_trend)
    
    assert forecasts['+15m'] == -27.5
    assert forecasts['+30m'] == -35.0
    assert forecasts['+45m'] == -42.5
    assert forecasts['+60m'] == -50.0
