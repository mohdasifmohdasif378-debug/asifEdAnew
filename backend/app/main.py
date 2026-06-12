from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.config import settings
from app.database import engine
from app.models import Base
from app.routers import auth_router, chat_router
from datetime import datetime
import time
Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
# Restrict CORS to configured frontend origins for better security
allowed = [origin.strip() for origin in settings.FRONTEND_ORIGINS.split(',') if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=allowed or ["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
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
def root(): return RedirectResponse(url="/index.html")
@app.get("/api/health")
def health(): return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
