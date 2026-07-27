from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class SiteBase(BaseModel):
    name: str
    country: str
    region: Optional[str] = None
    latitude: float
    longitude: float
    population: Optional[int] = 0
    households: Optional[int] = 0
    productive_use_type: Optional[str] = None
    current_diesel_consumption_l_per_day: Optional[float] = 0
    estimated_load_kw: Optional[float] = 0

class SiteCreate(SiteBase):
    pass

class SiteResponse(SiteBase):
    id: UUID
    solar_irradiance_kwh_m2: Optional[float] = None
    suitability_score: Optional[float] = None
    grid_distance_km: Optional[float] = None
    transmission_loss_percent: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class OptimizationInput(BaseModel):
    site_id: UUID
    solar_capacity_kw: float = Field(..., gt=0)
    battery_capacity_kwh: float = Field(..., gt=0)

class OptimizationResponse(BaseModel):
    site_id: UUID
    site_name: str
    predicted_diesel_savings_l_per_day: float
    predicted_co2_reduction_tons_per_year: float
    predicted_cost_savings_usd_per_year: float
    payback_period_years: float
    carbon_credit_revenue_usd_per_year: float

class RegulatoryMatrixResponse(BaseModel):
    country: str
    tariff_approval_time_score: int
    import_duty_on_solar_score: int
    local_content_requirement_score: int
    land_acquisition_score: int
    grid_connection_policy_score: int
    overall_regulatory_friction_score: float
