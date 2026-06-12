from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserLogin, Token, ErrorResponse
from app.auth import hash_password, authenticate_user, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user. Username must be 3-50 alphanumeric chars, password 4-100 chars."""
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(400, detail="Username already registered")
    try:
        user = User(username=user_data.username, hashed_password=hash_password(user_data.password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return Token(access_token=create_access_token(data={"sub": user.username}))
    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail="Registration failed")

@router.post("/login", response_model=Token, responses={401: {"model": ErrorResponse}})
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with username and password to get JWT token."""
    user = authenticate_user(db, user_data.username.lower(), user_data.password)
    if not user:
        raise HTTPException(401, detail="Incorrect username or password")
    return Token(access_token=create_access_token(data={"sub": user.username}))

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    """Validate JWT token and return current user info."""
    return {"username": current_user.username}
