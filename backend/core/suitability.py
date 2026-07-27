import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from geoalchemy2.functions import ST_Distance, ST_SetSRID, ST_MakePoint
from sqlalchemy import func
from database import SessionLocal
from models import Site

class SuitabilityEngine:
    """
    Computes site suitability scores using weighted overlay analysis.
    All weights align with ECREEE's strategic priorities.
    """
    
    # Weights (sum = 1.0) - ECREEE-aligned
    WEIGHTS = {
        "solar_irradiance": 0.35,      # Solar resource quality
        "grid_distance": 0.25,          # Avoid transmission losses
        "population_density": 0.20,      # Impact on people
        "productive_use": 0.15,          # Economic impact
        "road_access": 0.05              # Accessibility
    }
    
    @classmethod
    def compute_suitability(cls, site_data: Dict) -> float:
        """
        Compute weighted suitability score for a single site.
        Score range: 0-100 (higher = more suitable).
        """
        scores = {}
        
        # Solar irradiance (normalized: 4-7 kWh/m²/day → 0-100)
        solar = site_data.get("solar_irradiance_kwh_m2", 4.5)
        scores["solar_irradiance"] = min(100, max(0, (solar - 4.0) / 3.0 * 100))
        
        # Grid distance (closer = better for grid-tied, but remote = better for mini-grid)
        # We incentivize sites 5-20km from grid (optimal for mini-grids)
        grid_dist = site_data.get("grid_distance_km", 50)
        if grid_dist < 2:
            scores["grid_distance"] = 20  # Too close to existing grid
        elif 2 <= grid_dist <= 5:
            scores["grid_distance"] = 60
        elif 5 < grid_dist <= 20:
            scores["grid_distance"] = 100  # Sweet spot
        elif 20 < grid_dist <= 50:
            scores["grid_distance"] = 60
        else:
            scores["grid_distance"] = 20  # Too remote
            
        # Population density (normalized: 0-5000 people/km²)
        pop_density = site_data.get("population_density", 100)
        scores["population_density"] = min(100, (pop_density / 5000) * 100)
        
        # Productive use (health = 100, agro-processing = 80, education = 60, other = 40)
        use_type = site_data.get("productive_use_type", "other")
        use_scores = {
            "health": 100,
            "agro_processing": 80,
            "education": 60,
            "commercial": 50,
            "other": 40
        }
        scores["productive_use"] = use_scores.get(use_type, 40)
        
        # Road access (distance to nearest road)
        road_dist = site_data.get("road_distance_km", 10)
        scores["road_access"] = min(100, max(0, (1 - road_dist / 20) * 100))
        
        # Weighted sum
        total = sum(
            scores[key] * cls.WEIGHTS[key] 
            for key in cls.WEIGHTS.keys()
        )
        
        return round(total, 1)
    
    @classmethod
    def get_top_sites(cls, country: str = None, limit: int = 10) -> List[Dict]:
        """
        Query database and return top N sites by suitability score.
        """
        session = SessionLocal()
        try:
            query = session.query(Site)
            if country:
                query = query.filter(Site.country == country)
            query = query.order_by(Site.suitability_score.desc()).limit(limit)
            
            return [
                {
                    "id": str(s.id),
                    "name": s.name,
                    "country": s.country,
                    "latitude": s.latitude,
                    "longitude": s.longitude,
                    "suitability_score": s.suitability_score,
                    "solar_irradiance": s.solar_irradiance_kwh_m2,
                    "grid_distance_km": s.grid_distance_km
                }
                for s in query.all()
            ]
        finally:
            session.close()
