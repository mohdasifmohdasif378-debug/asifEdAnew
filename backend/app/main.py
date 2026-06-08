from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.config import settings
from app.database import engine
from app.models import Base
from app.routers import auth_router, chat_router
Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router.router, prefix="/api")
app.include_router(chat_router.router, prefix="/api")
@app.get("/")
def root(): return RedirectResponse(url="/index.html")
@app.get("/api/health")
def health(): return {"status": "healthy"}
