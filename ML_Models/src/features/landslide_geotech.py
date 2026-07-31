import math

class LandslideGeotech:
    def __init__(self):
        # Target high hazard sectors
        self.target_sectors = ["Cerro Grande", "El Brillador", "Juan Soldado"]

    def calculate_factor_of_safety(self, c_prime, gamma, gamma_w, z, beta_deg, phi_prime_deg):
        """
        Calculate Factor of Safety (FS) using the Infinite Slope Model.
        c_prime: Effective cohesion (kPa)
        gamma: Unit weight of soil (kN/m^3)
        gamma_w: Unit weight of water (kN/m^3)
        z: Depth of sliding surface (m)
        beta_deg: Slope angle (degrees)
        phi_prime_deg: Effective friction angle (degrees)
        """
        beta = math.radians(beta_deg)
        phi_prime = math.radians(phi_prime_deg)

        # FS = (c' + (gamma - gamma_w) * z * cos^2(beta) * tan(phi')) / (gamma * z * sin(beta) * cos(beta))
        numerator = c_prime + (gamma - gamma_w) * z * (math.cos(beta) ** 2) * math.tan(phi_prime)
        denominator = gamma * z * math.sin(beta) * math.cos(beta)

        if denominator == 0:
            return float('inf')

        return numerator / denominator

    def evaluate_hazard(self, sector, c_prime, gamma, gamma_w, z, beta_deg, phi_prime_deg):
        """
        Evaluate landslide hazard for a specific sector.
        Flags True (Hazardous) if FS < 1.0 and sector is in target high slope sectors.
        """
        fs = self.calculate_factor_of_safety(c_prime, gamma, gamma_w, z, beta_deg, phi_prime_deg)
        
        is_hazard = fs < 1.0
        in_target_sector = sector in self.target_sectors
        
        return {
            "sector": sector,
            "factor_of_safety": fs,
            "hazard_flag": is_hazard and in_target_sector
        }
