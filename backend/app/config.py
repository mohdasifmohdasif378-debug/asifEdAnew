import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    # Application
    PROJECT_NAME: str = "ExamBrain - Competitive Exam Mastery Platform"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS & Allowed Hosts
    FRONTEND_ORIGINS: str = os.getenv("FRONTEND_ORIGINS", "http://localhost:3001,http://127.0.0.1:3001")
    ALLOWED_HOSTS: str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/exambrain.db")
    
    # AI & External APIs
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Rate Limiting (requests per minute)
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Security Features
    ENABLE_HTTPS_REDIRECT: bool = os.getenv("ENABLE_HTTPS_REDIRECT", "false").lower() == "true"
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_ATTEMPT_WINDOW_MINUTES: int = 15
    SESSION_TIMEOUT_MINUTES: int = 60

settings = Settings()
