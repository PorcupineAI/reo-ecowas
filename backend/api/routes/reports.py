from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import io

from backend.database import get_db
from backend.models.site import Site

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    sites = db.query(Site).all()
    return {
        "total": len(sites),
        "avg_suitability": sum(s.suitability_score or 0 for s in sites)/len(sites) if sites else 0
    }

@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    sites = db.query(Site).all()
    data = [{"name": s.name, "country": s.country, "score": s.suitability_score} for s in sites]
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=sites.csv"})
