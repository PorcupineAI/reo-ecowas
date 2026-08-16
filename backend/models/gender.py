from sqlalchemy import Column, String, Float, DateTime, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base
import uuid
from datetime import datetime

class GenderMetrics(Base):
    __tablename__ = "gender_metrics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    female_headed_households = Column(Integer, default=0)
    female_energy_entrepreneurs = Column(Integer, default=0)
    female_employees_percent = Column(Float, default=0)
    female_decision_makers_percent = Column(Float, default=0)
    women_using_clean_cooking = Column(Integer, default=0)
    girls_school_attendance_impact = Column(Float, default=0)
    women_income_generation = Column(Float, default=0)
    gender_consultations_completed = Column(Boolean, default=False)
    gender_action_plan_exists = Column(Boolean, default=False)
    safety_measures_for_women = Column(Boolean, default=False)
    women_targeted_beneficiary = Column(Boolean, default=False)
    gender_inclusion_score = Column(Float, default=0)
    gender_equality_index = Column(Float, default=0)
    sdg5_alignment_score = Column(Float, default=0)
    data_quality_score = Column(Float, default=0)
    data_collection_date = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GenderPolicyCompliance(Base):
    __tablename__ = "gender_policy_compliance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False, unique=True)
    gender_assessment_mandate = Column(Integer, default=1)
    gender_budgeting = Column(Integer, default=1)
    women_in_energy_ministry = Column(Integer, default=1)
    gender_data_collection = Column(Integer, default=1)
    community_consultation = Column(Integer, default=1)
    policy_alignment_score = Column(Float, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
