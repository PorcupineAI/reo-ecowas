#!/usr/bin/env python3
"""
Seed REO-ECOWAS database with sample sites and regulatory scores.
Uses the same database connection as the main application.
"""

import sys
import os
import random

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Site, RegulatoryScore
from backend.core.suitability import SuitabilityEngine


def seed_sites():
    db = SessionLocal()
    try:
        # Clear existing data (optional)
        db.query(Site).delete()
        db.query(RegulatoryScore).delete()

        # Sample sites
        sample_sites = [
            {
                "name": "Ago-Are Health Center",
                "country": "Nigeria",
                "lat": 8.5,
                "lon": 4.2,
                "pop": 5000,
                "type": "health"
            },
            {
                "name": "Kandi Agro-Processing",
                "country": "Benin",
                "lat": 10.5,
                "lon": 1.8,
                "pop": 12000,
                "type": "agro_processing"
            },
            {
                "name": "Sokode Community Grid",
                "country": "Togo",
                "lat": 8.0,
                "lon": 1.2,
                "pop": 8000,
                "type": "education"
            },
            {
                "name": "Wa Solar Mini-Grid",
                "country": "Ghana",
                "lat": 10.0,
                "lon": -2.5,
                "pop": 15000,
                "type": "commercial"
            },
            {
                "name": "Bouake Rice Mill",
                "country": "Côte d'Ivoire",
                "lat": 7.7,
                "lon": -5.0,
                "pop": 2000,
                "type": "agro_processing"
            }
        ]

        for s in sample_sites:
            site = Site(
                name=s["name"],
                country=s["country"],
                latitude=s["lat"],
                longitude=s["lon"],
                population=s["pop"],
                productive_use_type=s["type"],
                current_diesel_consumption_l_per_day=round(random.uniform(20, 80), 1),
                estimated_load_kw=round(random.uniform(5, 30), 1),
                solar_irradiance_kwh_m2=round(random.uniform(4.8, 5.8), 2),
                grid_distance_km=round(random.uniform(3, 35), 1)
            )
            # Compute suitability score
            site.suitability_score = SuitabilityEngine.compute_suitability({
                "solar_irradiance_kwh_m2": site.solar_irradiance_kwh_m2,
                "grid_distance_km": site.grid_distance_km,
                "population": site.population,
                "productive_use_type": site.productive_use_type
            })
            site.transmission_loss_percent = 35 + max(0, (site.grid_distance_km - 10) * 0.5)
            db.add(site)

        # Seed regulatory scores for ECOWAS countries
        countries = [
            "Nigeria", "Benin", "Togo", "Ghana", "Côte d'Ivoire",
            "Senegal", "Mali", "Burkina Faso", "Niger", "Guinea",
            "Liberia", "Sierra Leone", "The Gambia", "Cabo Verde", "Guinea-Bissau"
        ]
        for c in countries:
            reg = RegulatoryScore(
                country=c,
                tariff_approval_time_score=random.randint(2, 5),
                import_duty_on_solar_score=random.randint(2, 5),
                local_content_requirement_score=random.randint(2, 5),
                land_acquisition_score=random.randint(2, 5),
                grid_connection_policy_score=random.randint(2, 5)
            )
            friction = (
                (5 - reg.tariff_approval_time_score) +
                (5 - reg.import_duty_on_solar_score) +
                (5 - reg.local_content_requirement_score) +
                (5 - reg.land_acquisition_score) +
                (5 - reg.grid_connection_policy_score)
            )
            reg.overall_regulatory_friction_score = round(friction / 5, 2)
            db.add(reg)

        db.commit()
        print(f"✅ Seeded {len(sample_sites)} sites and {len(countries)} regulatory scores.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_sites()
