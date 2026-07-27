from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry  # PostGIS support
from config import settings

# Enable PostGIS extensions on connection
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"options": "-c search_path=public,postgis"},
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
