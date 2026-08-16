class GeospatialService:
    @staticmethod
    def enrich_site(site):
        site.solar_irradiance_kwh_m2 = 5.2
        site.grid_distance_km = 10.0
        site.transmission_loss_percent = 35
        return site
