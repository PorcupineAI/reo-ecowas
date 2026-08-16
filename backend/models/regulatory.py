from sqlalchemy import Column, Integer, Float, String
from backend.database import Base

class RegulatoryScore(Base):
    __tablename__ = "regulatory_scores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False, unique=True)
    tariff_approval_time_score = Column(Integer, default=3)
    import_duty_on_solar_score = Column(Integer, default=3)
    local_content_requirement_score = Column(Integer, default=3)
    land_acquisition_score = Column(Integer, default=3)
    grid_connection_policy_score = Column(Integer, default=3)
    overall_regulatory_friction_score = Column(Float, default=0)
