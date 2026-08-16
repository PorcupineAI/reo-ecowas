import numpy as np

class ForecastEngine:
    @classmethod
    def fetch_solar_forecast(cls, lat, lon):
        # Mock – replace with NASA POWER API
        return [max(0, 12 * np.sin(np.pi * (i/24)) + np.random.normal(0,0.5)) for i in range(96)]

    @classmethod
    def predict_load(cls, site_data):
        base = site_data.get("estimated_load_kw", 10)
        return [base * (0.5 + 0.5 * np.sin(np.pi * i/48)) for i in range(96)]
