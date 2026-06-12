from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import RedirectResponse
from app.config import settings
from app.database import engine
from app.models import Base
from app.routers import auth_router, chat_router
from datetime import datetime
import time

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Security Middleware Stack
# 1. HTTPS Redirect (production only)
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# 2. Trusted Hosts (prevent Host header attacks)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS.split(",") if settings.ALLOWED_HOSTS else ["localhost", "127.0.0.1"]
)

# 3. CORS (restrict to configured origins)
allowed = [origin.strip() for origin in settings.FRONTEND_ORIGINS.split(',') if origin.strip()]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=allowed or ["http://localhost:3001"],
    allow_credentials=True, 
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"]
)

# 4. Security Headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Enable XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # Referrer policy for privacy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # Content Security Policy
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    # Strict Transport Security (HTTPS)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # Permissions Policy
    response.headers["Permissions-Policy"] = "microphone=(), camera=(), geolocation=()"
    return response

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{datetime.utcnow().isoformat()} {request.method} {request.url.path} {response.status_code} {duration:.2f}s")
    return response

app.include_router(auth_router.router, prefix="/api")
app.include_router(chat_router.router, prefix="/api")

@app.get("/")
def root(): 
    return RedirectResponse(url="/index.html")

@app.get("/api/health")
def health(): 
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "version": settings.VERSION}
