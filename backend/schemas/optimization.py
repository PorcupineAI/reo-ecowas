from pydantic import BaseModel
from uuid import UUID

class OptimizationInput(BaseModel):
    site_id: UUID
    solar_capacity_kw: float
    battery_capacity_kwh: float

class OptimizationResponse(BaseModel):
    site_id: UUID
    site_name: str
    predicted_diesel_savings_l_per_day: float
    predicted_co2_reduction_tons_per_year: float
    predicted_cost_savings_usd_per_year: float
    payback_period_years: float
    carbon_credit_revenue_usd_per_year: float
