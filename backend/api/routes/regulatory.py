from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.regulatory import RegulatoryScore
from backend.schemas.regulatory import RegulatoryMatrixResponse

router = APIRouter(prefix="/regulatory", tags=["regulatory"])

@router.get("/", response_model=list[RegulatoryMatrixResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(RegulatoryScore).all()

@router.get("/{country}", response_model=RegulatoryMatrixResponse)
def get_country(country: str, db: Session = Depends(get_db)):
    rec = db.query(RegulatoryScore).filter(RegulatoryScore.country == country).first()
    if not rec:
        raise HTTPException(404, "Country not found")
    return rec
