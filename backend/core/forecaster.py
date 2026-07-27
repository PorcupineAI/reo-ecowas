import pandas as pd
import numpy as np
from typing import Tuple, List
from datetime import datetime, timedelta
import requests
from config import settings
import logging

logger = logging.getLogger(__name__)

class ForecastEngine:
    """
    Generates 24-hour ahead forecasts for solar irradiance and load demand.
    Uses NASA POWER API for solar and a persistence/seasonal model for load.
    """
    
    @classmethod
    def fetch_solar_forecast(cls, latitude: float, longitude: float) -> List[float]:
        """
        Fetch 24-hour solar irradiance (kW per 15-min) from NASA POWER API.
        Returns 96 values (15-min intervals).
        """
        try:
            # NASA POWER API for solar irradiance (kW/m²)
            url = f"{settings.NASA_POWER_API}/power/v2/point"
            params = {
                "parameters": "ALLSKY_SFC_SW_DWN",
                "latitude": latitude,
                "longitude": longitude,
                "start": (datetime.now() - timedelta(days=1)).strftime("%Y%m%d"),
                "end": (datetime.now() + timedelta(days=1)).strftime("%Y%m%d"),
                "format": "JSON"
            }
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            # Extract values (W/m²) and convert to kW for a 10kW system approximation
            raw = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
            times = sorted(raw.keys())
            values = [raw[t] for t in times]
            
            # Interpolate to 96 intervals (15-min)
            if len(values) == 96:
                return [v / 1000 * 5 for v in values]  # Approx 5m² panel area for 10kW peak
            
            # Fallback: synthetic curve if API fails
            return cls._generate_synthetic_solar()
            
        except Exception as e:
            logger.error(f"NASA POWER API failed: {e}. Using synthetic.")
            return cls._generate_synthetic_solar()
    
    @classmethod
    def _generate_synthetic_solar(cls) -> List[float]:
        """Generate a typical solar curve (daylight hours only)."""
        values = []
        for i in range(96):
            hour = i / 4  # 0-24
            # Sine curve peaking at solar noon (12 PM)
            if 5 <= hour <= 19:
                val = max(0, np.sin(np.pi * (hour - 5) / 14)) * 12
            else:
                val = 0
            # Add random noise
            values.append(max(0, val + np.random.normal(0, 0.5)))
        return values
    
    @classmethod
    def predict_load(cls, site_data: dict, historical_load: List[float] = None) -> List[float]:
        """
        Predict 24-hour load profile (15-min intervals).
        Uses a simple weekday/weekend seasonal average.
        """
        if historical_load and len(historical_load) >= 96:
            # Use last 96 intervals as baseline (persistence)
            return historical_load[-96:]
        
        # Fallback: Create a typical load shape based on site type
        base_load = site_data.get("estimated_load_kw", 10)
        use_type = site_data.get("productive_use_type", "other")
        
        # Load shape profiles (normalized)
        if use_type == "health":
            profile = [0.8] * 96  # Constant load
        elif use_type == "agro_processing":
            profile = [0.2] * 20 + [1.0] * 12 + [0.3] * 64  # Mid-day peak
        else:  # Residential / mixed
            profile = [0.3] * 32 + [0.7] * 32 + [0.4] * 32  # Morning/evening peaks
        
        # Scale to base load
        scaled = [base_load * p for p in profile]
        return scaled
