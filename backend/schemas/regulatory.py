from pydantic import BaseModel

class RegulatoryMatrixResponse(BaseModel):
    country: str
    tariff_approval_time_score: int
    import_duty_on_solar_score: int
    local_content_requirement_score: int
    land_acquisition_score: int
    grid_connection_policy_score: int
    overall_regulatory_friction_score: float

    class Config:
        from_attributes = True
