import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.scheduler.tasks import start_scheduler
from backend.api.routes import (
    sites,
    optimization,
    reports,
    regulatory,
    gender,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting REO-ECOWAS...")
    # Schema managed by Alembic – no create_all()
    start_scheduler()
    logger.info("✅ Scheduler started.")
    yield
    logger.info("🛑 Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = settings.API_V1_PREFIX
app.include_router(sites.router, prefix=api_prefix, tags=["sites"])
app.include_router(optimization.router, prefix=api_prefix, tags=["optimization"])
app.include_router(reports.router, prefix=api_prefix, tags=["reports"])
app.include_router(regulatory.router, prefix=api_prefix, tags=["regulatory"])
app.include_router(gender.router, prefix=api_prefix, tags=["gender"])


@app.get("/health")
async def health():
    return {"status": "healthy", "service": settings.PROJECT_NAME}


@app.get("/")
async def root():
    return {"service": settings.PROJECT_NAME, "version": settings.VERSION, "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
