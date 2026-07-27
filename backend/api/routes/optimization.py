from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from models import Site, OptimizationRun
from schemas import OptimizationInput, OptimizationResponse
from core.optimizer import EnergyOptimizer
from core.carbon import CarbonFinanceCalculator

router = APIRouter(prefix="/optimize", tags=["optimization"])

@router.post("/", response_model=OptimizationResponse)
def run_optimization(
    input_data: OptimizationInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Run dispatch optimization for a site.
    Returns cost savings, CO2 reduction, and carbon credit potential.
    """
    site = db.query(Site).filter(Site.id == input_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # TODO: Fetch actual solar/load forecasts from API
    # Using mock data for demonstration
    import numpy as np
    solar_forecast = np.random.uniform(0, 15, 96).tolist()  # 15-min intervals
    load_forecast = np.random.uniform(5, 20, 96).tolist()
    
    # Run optimization
    optimizer = EnergyOptimizer(
        site_id=str(site.id),
        solar_forecast=solar_forecast,
        load_forecast=load_forecast
    )
    result = optimizer.optimize()
    
    if result["status"] != "optimal":
        raise HTTPException(status_code=400, detail="Optimization failed: " + result.get("error", ""))
    
    # Calculate baseline (diesel-only scenario)
    baseline_diesel = site.current_diesel_consumption_l_per_day or 50  # Default if not set
    optimized_diesel = result["total_diesel_liters"] / 96 * 24  # Convert to per day
    
    # Carbon finance calculation
    carbon = CarbonFinanceCalculator.calculate_avoided_emissions(
        baseline_diesel_l_per_day=baseline_diesel,
        optimized_diesel_l_per_day=optimized_diesel
    )
    
    # Save optimization run to database
    run = OptimizationRun(
        site_id=site.id,
        solar_capacity_kw=input_data.solar_capacity_kw,
        battery_capacity_kwh=input_data.battery_capacity_kwh,
        predicted_diesel_savings_l_per_day=baseline_diesel - optimized_diesel,
        predicted_co2_reduction_tons_per_year=carbon["avoided_co2_tons_per_year"],
        predicted_cost_savings_usd_per_year=(baseline_diesel - optimized_diesel) * 365 * 0.85,
        payback_period_years=5.0,  # TODO: Compute from CAPEX
        carbon_credit_revenue_usd_per_year=carbon["carbon_credit_revenue_usd"],
        status="completed"
    )
    db.add(run)
    db.commit()
    
    return OptimizationResponse(
        site_id=site.id,
        site_name=site.name,
        predicted_diesel_savings_l_per_day=baseline_diesel - optimized_diesel,
        predicted_co2_reduction_tons_per_year=carbon["avoided_co2_tons_per_year"],
        predicted_cost_savings_usd_per_year=(baseline_diesel - optimized_diesel) * 365 * 0.85,
        payback_period_years=5.0,
        carbon_credit_revenue_usd_per_year=carbon["carbon_credit_revenue_usd"]
    )
