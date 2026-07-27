from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database import get_db
from models import Site
from schemas import SiteCreate, SiteResponse
from core.suitability import SuitabilityEngine

router = APIRouter(prefix="/sites", tags=["sites"])

@router.get("/", response_model=List[SiteResponse])
def get_sites(
    country: Optional[str] = None,
    min_score: Optional[float] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all sites with optional filters."""
    query = db.query(Site)
    if country:
        query = query.filter(Site.country == country)
    if min_score:
        query = query.filter(Site.suitability_score >= min_score)
    return query.order_by(Site.suitability_score.desc()).limit(limit).all()

@router.get("/top", response_model=List[SiteResponse])
def get_top_sites(
    country: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get top N sites by suitability score."""
    query = db.query(Site)
    if country:
        query = query.filter(Site.country == country)
    return query.order_by(Site.suitability_score.desc()).limit(limit).all()

@router.post("/", response_model=SiteResponse)
def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    """Create a new site with automatic suitability scoring."""
    db_site = Site(**site.model_dump())
    
    # Auto-compute suitability
    site_data = site.model_dump()
    site_data["solar_irradiance_kwh_m2"] = 5.2  # TODO: Fetch from NASA POWER API
    site_data["grid_distance_km"] = 10.0  # TODO: Compute from WAPP data
    db_site.suitability_score = SuitabilityEngine.compute_suitability(site_data)
    
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.get("/{site_id}", response_model=SiteResponse)
def get_site(site_id: UUID, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site
