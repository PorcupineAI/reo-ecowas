from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.database import get_db
from backend.models.site import Site
from backend.schemas.optimization import OptimizationInput, OptimizationResponse
from backend.core.optimizer import EnergyOptimizer
from backend.core.carbon import CarbonFinanceCalculator
from backend.core.forecaster import ForecastEngine

router = APIRouter(prefix="/optimize", tags=["optimization"])

@router.post("/", response_model=OptimizationResponse)
def run_optimization(
    data: OptimizationInput,
    db: Session = Depends(get_db)
):
    site = db.query(Site).filter(Site.id == data.site_id).first()
    if not site:
        raise HTTPException(404, "Site not found")

    solar = ForecastEngine.fetch_solar_forecast(site.latitude, site.longitude)
    load = ForecastEngine.predict_load({"estimated_load_kw": site.estimated_load_kw})

    opt = EnergyOptimizer(str(site.id), solar, load)
    result = opt.optimize()

    if result["status"] != "optimal":
        raise HTTPException(400, "Optimization failed")

    baseline_diesel = site.current_diesel_consumption_l_per_day or 50
    optimized_diesel = result["total_diesel_liters"] / 96 * 24
    co2 = CarbonFinanceCalculator.calculate_avoided_emissions(
        baseline_diesel_l_per_day=baseline_diesel,
        optimized_diesel_l_per_day=optimized_diesel
    )

    return OptimizationResponse(
        site_id=site.id,
        site_name=site.name,
        predicted_diesel_savings_l_per_day=baseline_diesel - optimized_diesel,
        predicted_co2_reduction_tons_per_year=co2["avoided_co2_tons_per_year"],
        predicted_cost_savings_usd_per_year=(baseline_diesel - optimized_diesel)*365*0.85,
        payback_period_years=5.0,
        carbon_credit_revenue_usd_per_year=co2["carbon_credit_revenue_usd"]
)
