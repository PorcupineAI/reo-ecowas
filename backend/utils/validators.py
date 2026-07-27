from pydantic import BaseModel, Field, validator
import re

class CoordinatesValidator(BaseModel):
    """Reusable coordinate validation."""
    
    @validator("latitude")
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v
    
    @validator("longitude")
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v

class CountryCodeValidator(BaseModel):
    """Validate ECOWAS country names or codes."""
    
    ECOWAS_COUNTRIES = {
        "NG", "BJ", "TG", "GH", "CI", "SN", "ML", "BF", "NE", 
        "GN", "LR", "SL", "GM", "CV", "GW"
    }
    
    @validator("country")
    def validate_ecowas_country(cls, v):
        v_upper = v.upper()
        if v_upper not in cls.ECOWAS_COUNTRIES and v.title() not in [
            "Nigeria", "Benin", "Togo", "Ghana", "Côte d'Ivoire", "Ivory Coast",
            "Senegal", "Mali", "Burkina Faso", "Niger", "Guinea", "Liberia",
            "Sierra Leone", "The Gambia", "Gambia", "Cabo Verde", "Guinea-Bissau"
        ]:
            raise ValueError(f"'{v}' is not a recognized ECOWAS member state.")
        return v_upper

def sanitize_input(text: str, max_length: int = 255) -> str:
    """Basic input sanitization for free-text fields."""
    if not text:
        return ""
    # Strip HTML tags, limit length
    clean = re.sub(r'<[^>]*>', '', text)
    return clean[:max_length].strip()
