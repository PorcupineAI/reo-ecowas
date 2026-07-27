#!/usr/bin/env python3
"""
CLI tool to run the energy optimization for a given site.
Usage: python scripts/run_optimization.py --site-id <uuid> --solar 50 --battery 100
"""

import sys
import os
import argparse
import json
from uuid import UUID

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Site, OptimizationRun
from backend.core.optimizer import EnergyOptimizer
from backend.core.forecaster import ForecastEngine
from backend.core.carbon import CarbonFinanceCalculator
from backend.services.geospatial import GeospatialService


def run_optimization_cli(site_id: str, solar_kw: float, battery_kwh: float, output_json: bool = False):
    """
    Main CLI entry point.
    """
    db = SessionLocal()
    try:
        # Fetch site
        site = db.query(Site).filter(Site.id == UUID(site_id)).first()
        if not site:
            print(f"❌ Error: Site with ID {site_id} not found.")
            return 1

        print(f"🔍 Running optimization for: {site.name} ({site.country})")
        print(f"   Solar: {solar_kw} kW | Battery: {battery_kwh} kWh")

        # Fetch forecasts
        solar_forecast = ForecastEngine.fetch_solar_forecast(site.latitude, site.longitude)
        load_forecast = ForecastEngine.predict_load({
            "estimated_load_kw": site.estimated_load_kw,
            "productive_use_type": site.productive_use_type
        })

        # Run optimizer
        optimizer = EnergyOptimizer(
            site_id=str(site.id),
            solar_forecast=solar_forecast,
            load_forecast=load_forecast
        )
        result = optimizer.optimize()

        if result["status"] != "optimal":
            print(f"❌ Optimization failed: {result.get('error', 'Unknown error')}")
            return 1

        # Baseline diesel (default 50 L/day if not recorded)
        baseline_diesel = site.current_diesel_consumption_l_per_day or 50.0
        optimized_diesel = result["total_diesel_liters"] / 96 * 24  # convert to per day

        # Carbon finance
        carbon = CarbonFinanceCalculator.calculate_avoided_emissions(
            baseline_diesel_l_per_day=baseline_diesel,
            optimized_diesel_l_per_day=optimized_diesel
        )

        # Compute annual savings
        annual_diesel_savings = (baseline_diesel - optimized_diesel) * 365
        annual_cost_savings = annual_diesel_savings * 0.85  # $0.85/L
        capex_estimate = solar_kw * 800 + battery_kwh * 300
        payback = capex_estimate / (annual_cost_savings + carbon["carbon_credit_revenue_usd"]) if (annual_cost_savings + carbon["carbon_credit_revenue_usd"]) > 0 else 0

        # Save to DB
        opt_run = OptimizationRun(
            site_id=site.id,
            solar_capacity_kw=solar_kw,
            battery_capacity_kwh=battery_kwh,
            predicted_diesel_savings_l_per_day=baseline_diesel - optimized_diesel,
            predicted_co2_reduction_tons_per_year=carbon["avoided_co2_tons_per_year"],
            predicted_cost_savings_usd_per_year=annual_cost_savings,
            payback_period_years=round(payback, 1),
            carbon_credit_revenue_usd_per_year=carbon["carbon_credit_revenue_usd"],
            status="completed"
        )
        db.add(opt_run)
        db.commit()

        # Output
        output = {
            "site": site.name,
            "country": site.country,
            "diesel_savings_l_per_day": round(baseline_diesel - optimized_diesel, 1),
            "co2_reduction_tons_per_year": round(carbon["avoided_co2_tons_per_year"], 2),
            "cost_savings_usd_per_year": round(annual_cost_savings, 0),
            "carbon_credit_revenue_usd_per_year": round(carbon["carbon_credit_revenue_usd"], 0),
            "payback_period_years": round(payback, 1),
            "capex_estimate_usd": round(capex_estimate, 0)
        }

        if output_json:
            print(json.dumps(output, indent=2))
        else:
            print("\n📊 OPTIMIZATION RESULTS")
            print("-" * 40)
            for k, v in output.items():
                print(f"  {k.replace('_', ' ').title()}: {v}")

        return 0

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        db.rollback()
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run REO-ECOWAS energy optimization for a site.")
    parser.add_argument("--site-id", required=True, help="UUID of the site")
    parser.add_argument("--solar", type=float, required=True, help="Solar capacity in kW")
    parser.add_argument("--battery", type=float, required=True, help="Battery capacity in kWh")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    sys.exit(run_optimization_cli(args.site_id, args.solar, args.battery, args.json))
