import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/reo")
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "REO-ECOWAS"
    VERSION: str = "1.0.0"
    
    # Security (for production)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External APIs
    NASA_POWER_API: str = "https://power.larc.nasa.gov/api"
    OPEN_METEO_API: str = "https://archive-api.open-meteo.com/v1"
    
    # Carbon pricing (World Bank average)
    CARBON_PRICE_USD_PER_TON: float = 35.0
    
    # Optimization defaults
    DEFAULT_DIESEL_COST_USD_PER_L: float = 0.85
    DEFAULT_BATTERY_DEGRADATION_COST: float = 0.02  # per kWh cycled
    
    class Config:
        env_file = ".env"

settings = Settings()
