from pydantic import BaseModel, Field, validator

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    @validator('message')
    def sanitize_message(cls, v):
        v = v.strip()[:4000]
        if not v:
            raise ValueError('Message cannot be empty after stripping')
        return v

class ChatResponse(BaseModel):
    reply: str

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=128)
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ErrorResponse(BaseModel):
    detail: str
