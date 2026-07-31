import numpy as np

class NowcastingEngine:
    def __init__(self, a=200, b=1.6):
        """
        Initialize Nowcasting Engine.
        Default parameters are for Marshall-Palmer Z-R relation: Z = a * R^b
        """
        self.a = a
        self.b = b

    def dbz_to_rain_rate(self, dbz):
        """
        Convert Radar Reflectivity (dBZ) to Rain Rate (mm/h) using Marshall-Palmer relation.
        Z = 10^(dBZ/10)
        R = (Z/a)^(1/b)
        """
        z_linear = 10 ** (dbz / 10.0)
        rain_rate = (z_linear / self.a) ** (1 / self.b)
        return rain_rate

    def extrapolate_ir_temperature(self, current_temp, temp_trend, lead_times=[15, 30, 45, 60]):
        """
        Extrapolate IR brightness temperature based on current trend (temp change per minute).
        lead_times: List of forecast lead times in minutes.
        Returns a dictionary of forecasts.
        """
        forecasts = {}
        for lt in lead_times:
            forecasts[f'+{lt}m'] = current_temp + (temp_trend * lt)
        return forecasts
