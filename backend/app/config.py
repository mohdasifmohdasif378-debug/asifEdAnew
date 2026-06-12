import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    PROJECT_NAME: str = "ASIFEDA AI"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "asifeda-default-change-me-in-production")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    # Comma-separated list of allowed frontend origins for CORS
    FRONTEND_ORIGINS: str = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./asifeda.db")
settings = Settings()
