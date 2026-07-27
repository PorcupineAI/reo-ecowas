from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import pandas as pd
import io
import json

from database import get_db
from models import Site, OptimizationRun, RegulatoryScore

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def get_summary_report(
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Generate a summary dashboard report in JSON."""
    query = db.query(Site)
    if country:
        query = query.filter(Site.country == country)
    
    sites = query.all()
    
    # Aggregate statistics
    total_sites = len(sites)
    avg_suitability = sum(s.suitability_score for s in sites) / total_sites if total_sites > 0 else 0
    
    # Optimization metrics
    opt_runs = db.query(OptimizationRun).all()
    total_co2_saved = sum(r.predicted_co2_reduction_tons_per_year for r in opt_runs)
    total_cost_saved = sum(r.predicted_cost_savings_usd_per_year for r in opt_runs)
    
    report = {
        "generated_at": pd.Timestamp.now().isoformat(),
        "country_filter": country or "All ECOWAS",
        "site_metrics": {
            "total_sites": total_sites,
            "average_suitability_score": round(avg_suitability, 1),
            "top_sites": [
                {"name": s.name, "score": s.suitability_score, "country": s.country}
                for s in sorted(sites, key=lambda x: x.suitability_score or 0, reverse=True)[:5]
            ]
        },
        "optimization_impact": {
            "total_co2_reduction_tons_per_year": round(total_co2_saved, 2),
            "total_cost_savings_usd_per_year": round(total_cost_saved, 2),
            "avg_payback_years": round(sum(r.payback_period_years for r in opt_runs) / len(opt_runs), 1) if opt_runs else 0
        },
        "recommendations": [
            f"Prioritize {s.name} ({s.country}) with score {s.suitability_score}" 
            for s in sorted(sites, key=lambda x: x.suitability_score or 0, reverse=True)[:3]
        ]
    }
    return JSONResponse(report)

@router.get("/export/csv")
def export_sites_csv(
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export site data as CSV for ECREEE working groups."""
    query = db.query(Site)
    if country:
        query = query.filter(Site.country == country)
    
    sites = query.all()
    data = [{
        "name": s.name,
        "country": s.country,
        "latitude": s.latitude,
        "longitude": s.longitude,
        "population": s.population,
        "suitability_score": s.suitability_score,
        "solar_irradiance_kwh": s.solar_irradiance_kwh_m2,
        "grid_distance_km": s.grid_distance_km,
        "transmission_loss_%": s.transmission_loss_percent
    } for s in sites]
    
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=reo_ecowas_sites.csv"}
    )
