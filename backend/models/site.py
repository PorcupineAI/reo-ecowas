from sqlalchemy import Column, String, Float, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from backend.database import Base
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
    population = Column(Integer, default=0)
    households = Column(Integer, default=0)
    productive_use_type = Column(String(100))
    current_diesel_consumption_l_per_day = Column(Float, default=0)
    estimated_load_kw = Column(Float, default=0)
    solar_irradiance_kwh_m2 = Column(Float)
    suitability_score = Column(Float)
    grid_distance_km = Column(Float)
    transmission_loss_percent = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
