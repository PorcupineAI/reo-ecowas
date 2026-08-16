from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.database import get_db
from backend.models.site import Site
from backend.schemas.site import SiteCreate, SiteResponse
from backend.core.suitability import SuitabilityEngine

router = APIRouter(prefix="/sites", tags=["sites"])

@router.get("/", response_model=List[SiteResponse])
def list_sites(
    country: Optional[str] = None,
    min_score: Optional[float] = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Site)
    if country:
        query = query.filter(Site.country == country)
    if min_score is not None:
        query = query.filter(Site.suitability_score >= min_score)
    return query.order_by(Site.suitability_score.desc()).limit(limit).all()

@router.get("/top", response_model=List[SiteResponse])
def top_sites(
    country: Optional[str] = None,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Site)
    if country:
        query = query.filter(Site.country == country)
    return query.order_by(Site.suitability_score.desc()).limit(limit).all()

@router.post("/", response_model=SiteResponse)
def create_site(
    site: SiteCreate,
    db: Session = Depends(get_db)
):
    db_site = Site(**site.dict())
    db_site.suitability_score = SuitabilityEngine.compute_suitability(db_site.__dict__)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.get("/{site_id}", response_model=SiteResponse)
def get_site(site_id: UUID, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(404, "Site not found")
    return site
