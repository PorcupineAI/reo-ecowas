from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import engine, Base
from api.routes import sites, optimization, reports, regulatory

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize scheduler
    from scheduler.tasks import start_scheduler
    start_scheduler()
    yield
    # Shutdown: Clean up

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(sites.router, prefix=settings.API_V1_PREFIX)
app.include_router(optimization.router, prefix=settings.API_V1_PREFIX)
app.include_router(reports.router, prefix=settings.API_V1_PREFIX)
app.include_router(regulatory.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"message": "REO-ECOWAS API", "version": settings.VERSION}

@app.get("/health")
def health():
    return {"status": "healthy"}
