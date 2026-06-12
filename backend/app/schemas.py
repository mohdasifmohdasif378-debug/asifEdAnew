from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

# Chat Schemas
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

# Auth Schemas
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)
    email: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must be alphanumeric with _ or - only')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# Error Response
class ErrorResponse(BaseModel):
    detail: str

# Notes Schemas
class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=50000)
    topic_id: Optional[int] = None
    is_public: bool = False

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_public: Optional[bool] = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    topic_id: Optional[int]
    is_public: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# Question Schemas
class QuestionResponse(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: str
    year: Optional[int]
    source: Optional[str]
    class Config:
        from_attributes = True

class QuestionWithAnswer(QuestionResponse):
    correct_answer: str
    explanation: Optional[str]

# Topic Schemas
class TopicResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    weightage: float
    difficulty: str
    class Config:
        from_attributes = True

# Subject Schemas
class SubjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    weightage: float
    class Config:
        from_attributes = True

# Exam Schemas
class ExamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class Config:
        from_attributes = True

# Progress Schemas
class ProgressResponse(BaseModel):
    topic_id: int
    total_questions: int
    correct_answers: int
    accuracy: float
    last_attempted: datetime
    class Config:
        from_attributes = True
