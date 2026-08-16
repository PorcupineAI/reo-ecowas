from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.database import get_db
from backend.models.gender import GenderMetrics, GenderPolicyCompliance
from backend.schemas.gender import GenderMetricsCreate, GenderMetricsResponse, GenderPolicyComplianceResponse
from backend.core.gender import GenderInclusionEngine

router = APIRouter(prefix="/gender", tags=["gender"])

@router.get("/sites/{site_id}", response_model=GenderMetricsResponse)
def get_metrics(site_id: UUID, db: Session = Depends(get_db)):
    m = db.query(GenderMetrics).filter(GenderMetrics.site_id == site_id).first()
    if not m:
        raise HTTPException(404, "No gender data found")
    return m

@router.post("/sites/{site_id}", response_model=GenderMetricsResponse)
def create_metrics(site_id: UUID, data: GenderMetricsCreate, db: Session = Depends(get_db)):
    existing = db.query(GenderMetrics).filter(GenderMetrics.site_id == site_id).first()
    if existing:
        raise HTTPException(400, "Already exists")
    metrics = GenderMetrics(site_id=site_id, **data.dict())
    metrics.gender_inclusion_score = GenderInclusionEngine.compute_gender_inclusion_score(data.dict())
    db.add(metrics)
    db.commit()
    db.refresh(metrics)
    return metrics

@router.get("/policy/{country}", response_model=GenderPolicyComplianceResponse)
def get_policy(country: str, db: Session = Depends(get_db)):
    rec = db.query(GenderPolicyCompliance).filter(GenderPolicyCompliance.country == country).first()
    if not rec:
        raise HTTPException(404, "Policy data not found")
    return rec
