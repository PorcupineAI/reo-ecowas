from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "REO-ECOWAS"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "change-me"
    CORS_ORIGINS: List[str] = ["*"]

    # Database – individual vars
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "reo"
    DATABASE_USER: str = "reo_user"
    DATABASE_PASSWORD: str = ""

    # External APIs
    NASA_POWER_API: str = "https://power.larc.nasa.gov/api"
    CARBON_PRICE_USD_PER_TON: float = 35.0
    GENDER_MODULE_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
