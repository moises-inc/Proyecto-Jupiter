import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ingesters.ingest_ceazamet import (
    parse_ceazamet_html,
    fetch_ceazamet_station_data,
    get_ceazamet_ground_truth_summary,
    CEAZAMET_STATIONS,
    _parse_numeric
)
from models.data_assimilation_enkf import EnsembleKalmanFilter, assimilate_iot_observations


SAMPLE_HTML = """
<table class="estacion">
<tr><td>Precipitación</td><td>12.5 mm</td></tr>
<tr><td>Temperatura</td><td>18.3 °C</td></tr>
<tr><td>Humedad</td><td>65 %</td></tr>
<tr><td>Velocidad del Viento</td><td>15.2 km/h</td></tr>
<tr><td>Dirección</td><td>SO</td></tr>
</table>
"""


class TestCeazametParsing:
    def test_parse_html_extracts_precipitation(self):
        parsed = parse_ceazamet_html(SAMPLE_HTML, "LSC")
        assert parsed["precipitation_mm"] == 12.5
        assert parsed["station_id"] == "LSC"

    def test_parse_html_extracts_temperature(self):
        parsed = parse_ceazamet_html(SAMPLE_HTML, "LSC")
        assert parsed["temperature_c"] == 18.3

    def test_parse_html_extracts_wind_speed(self):
        parsed = parse_ceazamet_html(SAMPLE_HTML, "LSC")
        assert parsed["wind_speed_kmh"] == 15.2

    def test_parse_html_extracts_humidity(self):
        parsed = parse_ceazamet_html(SAMPLE_HTML, "LSC")
        assert parsed["relative_humidity_pct"] == 65

    def test_parse_html_empty_table_returns_nones(self):
        empty_html = "<html><body><table></table></body></html>"
        parsed = parse_ceazamet_html(empty_html, "TEST")
        assert parsed["precipitation_mm"] is None
        assert parsed["temperature_c"] is None


class TestCeazametNumericParsing:
    def test_parse_simple_float(self):
        assert _parse_numeric("12.5") == 12.5

    def test_parse_with_unit(self):
        assert _parse_numeric("15.2 km/h") == 15.2

    def test_parse_comma_decimal(self):
        assert _parse_numeric("18,3") == 18.3

    def test_parse_empty_string_returns_none(self):
        assert _parse_numeric("") is None

    def test_parse_garbage_returns_none(self):
        assert _parse_numeric("N/A") is None


class TestCeazametStationsConfig:
    def test_all_stations_have_coordinates(self):
        for e_cod, info in CEAZAMET_STATIONS.items():
            assert "lat" in info
            assert "lon" in info
            assert "elevation_m" in info

    def test_all_stations_in_la_serena_region(self):
        for e_cod, info in CEAZAMET_STATIONS.items():
            assert -31 <= info["lat"] <= -29
            assert -72 <= info["lon"] <= -70


class TestCeazametFetchUnknownStation:
    def test_unknown_station_returns_available_false(self):
        result = fetch_ceazamet_station_data("INVALID")
        assert result["ceazamet_available"] is False
        assert "error" in result


class TestEnKFAassimilation:
    def test_assimilate_iot_observations_returns_innovation(self):
        enkf = EnsembleKalmanFilter(n_ensembles=50, state_dim=3, obs_dim=1)
        init_mean = np.array([5.0, 15.0, 10.0])
        init_cov = np.eye(3) * 1.0
        enkf.initialize_ensembles(init_mean, init_cov)
        corrected, innovation = assimilate_iot_observations(
            enkf,
            observed_precip_mm=12.5,
            forecast_precip_mm=8.0
        )
        assert isinstance(corrected, float)
        assert corrected >= 0.0

    def test_assimilate_iot_observations_with_no_rain(self):
        enkf = EnsembleKalmanFilter(n_ensembles=50, state_dim=3, obs_dim=1)
        init_mean = np.array([0.0, 15.0, 5.0])
        init_cov = np.eye(3) * 0.1
        enkf.initialize_ensembles(init_mean, init_cov)
        corrected, innovation = assimilate_iot_observations(
            enkf,
            observed_precip_mm=0.0,
            forecast_precip_mm=0.0
        )
        assert corrected == pytest.approx(0.0, abs=0.1)


class TestCeazametGroundTruthSummary:
    def test_summary_returns_dataframe_and_dict(self):
        df, summary = get_ceazamet_ground_truth_summary()
        assert isinstance(summary, dict)
        assert "ceazamet_available" in summary
        assert "timestamp" in summary
