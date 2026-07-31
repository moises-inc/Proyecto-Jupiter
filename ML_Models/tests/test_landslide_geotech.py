import pytest
import math
from src.features.landslide_geotech import LandslideGeotech

def test_calculate_factor_of_safety():
    geotech = LandslideGeotech()
    
    # Parameters that should yield an FS around 0.8 to 1.2 depending on calculation
    c_prime = 10.0 # kPa
    gamma = 20.0 # kN/m3
    gamma_w = 9.81 # kN/m3
    z = 2.0 # m
    beta_deg = 30.0 # degrees
    phi_prime_deg = 25.0 # degrees
    
    fs = geotech.calculate_factor_of_safety(c_prime, gamma, gamma_w, z, beta_deg, phi_prime_deg)
    
    # FS calculation check
    beta = math.radians(beta_deg)
    phi_prime = math.radians(phi_prime_deg)
    expected_fs = (c_prime + (gamma - gamma_w) * z * (math.cos(beta) ** 2) * math.tan(phi_prime)) / (gamma * z * math.sin(beta) * math.cos(beta))
    
    assert math.isclose(fs, expected_fs, rel_tol=1e-5)

def test_evaluate_hazard_true():
    geotech = LandslideGeotech()
    
    # Unstable conditions: FS < 1.0
    result = geotech.evaluate_hazard("Cerro Grande", c_prime=0.0, gamma=20.0, gamma_w=9.81, z=5.0, beta_deg=45.0, phi_prime_deg=20.0)
    
    assert result["factor_of_safety"] < 1.0
    assert result["hazard_flag"] is True

def test_evaluate_hazard_false_stable():
    geotech = LandslideGeotech()
    
    # Stable conditions: FS > 1.0
    result = geotech.evaluate_hazard("Cerro Grande", c_prime=50.0, gamma=20.0, gamma_w=9.81, z=1.0, beta_deg=10.0, phi_prime_deg=35.0)
    
    assert result["factor_of_safety"] >= 1.0
    assert result["hazard_flag"] is False

def test_evaluate_hazard_false_not_target():
    geotech = LandslideGeotech()
    
    # Unstable conditions but not in a target sector
    result = geotech.evaluate_hazard("La Serena Centro", c_prime=0.0, gamma=20.0, gamma_w=9.81, z=5.0, beta_deg=45.0, phi_prime_deg=20.0)
    
    assert result["factor_of_safety"] < 1.0
    assert result["hazard_flag"] is False
