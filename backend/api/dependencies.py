from typing import Optional
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal

def get_db():
    """Dependency: provides database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PaginationParams:
    """Common pagination parameters."""
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(50, ge=1, le=200, description="Max records to return")
    ):
        self.skip = skip
        self.limit = limit

def get_current_user():
    """
    Placeholder for future authentication.
    In production, implement JWT/OAuth2 against ECOWAS SSO.
    """
    return {"user_id": "system", "role": "programme_officer"}
