from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class GenderMetricsBase(BaseModel):
    female_headed_households: Optional[int] = 0
    female_energy_entrepreneurs: Optional[int] = 0
    female_employees_percent: Optional[float] = 0
    female_decision_makers_percent: Optional[float] = 0
    women_using_clean_cooking: Optional[int] = 0
    girls_school_attendance_impact: Optional[float] = 0
    women_income_generation: Optional[float] = 0
    gender_consultations_completed: Optional[bool] = False
    gender_action_plan_exists: Optional[bool] = False
    safety_measures_for_women: Optional[bool] = False
    women_targeted_beneficiary: Optional[bool] = False

class GenderMetricsCreate(GenderMetricsBase):
    pass

class GenderMetricsResponse(GenderMetricsBase):
    id: UUID
    site_id: UUID
    gender_inclusion_score: float
    gender_equality_index: float
    sdg5_alignment_score: float
    data_quality_score: float
    data_collection_date: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GenderPolicyComplianceResponse(BaseModel):
    country: str
    gender_assessment_mandate: int
    gender_budgeting: int
    women_in_energy_ministry: int
    gender_data_collection: int
    community_consultation: int
    policy_alignment_score: float
    updated_at: datetime

    class Config:
        from_attributes = True
