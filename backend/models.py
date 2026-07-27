from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from database import Base
import uuid
from datetime import datetime

class Site(Base):
    __tablename__ = "sites"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    region = Column(String(100))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geometry = Column(Geometry('POINT', srid=4326))
    
    # Site characteristics
    population = Column(Integer, default=0)
    households = Column(Integer, default=0)
    productive_use_type = Column(String(100))  # agro-processing, health, education
    
    # Energy data
    current_diesel_consumption_l_per_day = Column(Float, default=0)
    estimated_load_kw = Column(Float, default=0)
    existing_solar_kw = Column(Float, default=0)
    existing_battery_kwh = Column(Float, default=0)
    
    # Suitability scores (computed)
    solar_irradiance_kwh_m2 = Column(Float)
    suitability_score = Column(Float)
    grid_distance_km = Column(Float)
    transmission_loss_percent = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OptimizationRun(Base):
    __tablename__ = "optimization_runs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"))
    run_date = Column(DateTime, default=datetime.utcnow)
    
    # Inputs
    solar_capacity_kw = Column(Float)
    battery_capacity_kwh = Column(Float)
    
    # Outputs
    predicted_diesel_savings_l_per_day = Column(Float)
    predicted_co2_reduction_tons_per_year = Column(Float)
    predicted_cost_savings_usd_per_year = Column(Float)
    payback_period_years = Column(Float)
    carbon_credit_revenue_usd_per_year = Column(Float)
    
    # Status
    status = Column(String(50), default="completed")
    error_message = Column(Text)

class RegulatoryScore(Base):
    __tablename__ = "regulatory_scores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False, unique=True)
    
    # Scores 1-5 (5 = most favorable)
    tariff_approval_time_score = Column(Integer, default=3)
    import_duty_on_solar_score = Column(Integer, default=3)
    local_content_requirement_score = Column(Integer, default=3)
    land_acquisition_score = Column(Integer, default=3)
    grid_connection_policy_score = Column(Integer, default=3)
    
    # Composite
    overall_regulatory_friction_score = Column(Float)  # lower = better
