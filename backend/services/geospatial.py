import requests
import math
from typing import Dict
from models import Site
import logging

logger = logging.getLogger(__name__)

class GeospatialService:
    """Enrich site data with GIS-derived metrics."""
    
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance in km between two points."""
        R = 6371  # Earth radius
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return 2 * R * math.asin(math.sqrt(a))
    
    @classmethod
    def enrich_site(cls, site: Site) -> Site:
        """
        Add computed fields: solar irradiance, grid distance, transmission loss.
        """
        # 1. Solar Irradiance (Mock WAPP grid proximity for demo)
        # In production, call NASA POWER here.
        site.solar_irradiance_kwh_m2 = 5.2  # Average for West Africa
        
        # 2. Grid distance (simulate using centroid of major grid points)
        # For demo: random distance between 2 and 40 km
        import random
        site.grid_distance_km = round(random.uniform(2, 40), 1)
        
        # 3. Transmission loss (ECOWAS average 35%, increases with distance)
        base_loss = 35  # %
        if site.grid_distance_km > 20:
            base_loss += 10
        site.transmission_loss_percent = min(60, base_loss)
        
        return site
