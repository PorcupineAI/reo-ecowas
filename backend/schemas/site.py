from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

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
    solar_irradiance_kwh_m2: Optional[float]
    suitability_score: Optional[float]
    grid_distance_km: Optional[float]
    transmission_loss_percent: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
