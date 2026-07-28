from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import RegulatoryScore
from schemas import RegulatoryMatrixResponse

router = APIRouter(prefix="/regulatory", tags=["regulatory"])

@router.get("/", response_model=List[RegulatoryMatrixResponse])
def get_all_regulatory_scores(db: Session = Depends(get_db)):
    """Get regulatory scores for all ECOWAS countries."""
    scores = db.query(RegulatoryScore).all()
    return scores

@router.get("/{country}", response_model=RegulatoryMatrixResponse)
def get_regulatory_score(country: str, db: Session = Depends(get_db)):
    """Get regulatory score for a specific country."""
    score = db.query(RegulatoryScore).filter(RegulatoryScore.country == country).first()
    if not score:
        raise HTTPException(status_code=404, detail="Country not found")
    return score

@router.put("/{country}", response_model=RegulatoryMatrixResponse)
def update_regulatory_score(
    country: str,
    scores: dict,  # Expecting dict with score fields
    db: Session = Depends(get_db)
):
    """Update regulatory scores for a country (Programme Officer use)."""
    db_score = db.query(RegulatoryScore).filter(RegulatoryScore.country == country).first()
    if not db_score:
        raise HTTPException(status_code=404, detail="Country not found")
    
    # Update fields
    for key, value in scores.items():
        if hasattr(db_score, key):
            setattr(db_score, key, value)
    
    # Recompute overall friction score (lower = better)
    # Friction = (5 - tariff_score) + (5 - import_score) + ... 
    friction = (5 - db_score.tariff_approval_time_score) + \
               (5 - db_score.import_duty_on_solar_score) + \
               (5 - db_score.local_content_requirement_score) + \
               (5 - db_score.land_acquisition_score) + \
               (5 - db_score.grid_connection_policy_score)
    db_score.overall_regulatory_friction_score = round(friction / 5, 2)  # Normalized 0-4
    
    db.commit()
    db.refresh(db_score)
    return db_score
