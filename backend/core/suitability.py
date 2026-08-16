class SuitabilityEngine:
    WEIGHTS = {
        "solar_irradiance": 0.35,
        "grid_distance": 0.25,
        "population_density": 0.20,
        "productive_use": 0.15,
        "road_access": 0.05
    }

    @classmethod
    def compute_suitability(cls, site_data: dict) -> float:
        scores = {}
        solar = site_data.get("solar_irradiance_kwh_m2", 5.0)
        scores["solar_irradiance"] = min(100, max(0, (solar - 4.0) / 3.0 * 100))
        grid_dist = site_data.get("grid_distance_km", 20)
        if grid_dist < 2:
            scores["grid_distance"] = 20
        elif 2 <= grid_dist <= 5:
            scores["grid_distance"] = 60
        elif 5 < grid_dist <= 20:
            scores["grid_distance"] = 100
        else:
            scores["grid_distance"] = 40
        scores["population_density"] = min(100, site_data.get("population", 0) / 50)
        use_type = site_data.get("productive_use_type", "other")
        use_scores = {"health": 100, "agro_processing": 80, "education": 60, "other": 40}
        scores["productive_use"] = use_scores.get(use_type, 40)
        scores["road_access"] = 80  # dummy
        total = sum(scores[k] * cls.WEIGHTS[k] for k in cls.WEIGHTS.keys())
        return round(total, 1)
