from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")

class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # UPSC, SSC, NDA, Banking
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    subjects = relationship("Subject", back_populates="exam", cascade="all, delete-orphan")
    topics = relationship("Topic", back_populates="exam", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="exam", cascade="all, delete-orphan")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    name = Column(String, nullable=False, index=True)  # History, Geography, Economics, etc
    description = Column(Text, nullable=True)
    weightage = Column(Float, default=10.0)  # Percentage weightage in exam
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    exam = relationship("Exam", back_populates="subjects")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    weightage = Column(Float, default=5.0)  # Topic weightage within subject
    difficulty = Column(String, default="medium")  # easy, medium, hard
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    exam = relationship("Exam", back_populates="topics")
    subject = relationship("Subject", back_populates="topics")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)  # A, B, C, D
    explanation = Column(Text, nullable=True)
    difficulty = Column(String, default="medium")
    year = Column(Integer, nullable=True)  # Year of exam
    source = Column(String, nullable=True)  # Previous exam year
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    exam = relationship("Exam", back_populates="questions")
    topic = relationship("Topic", back_populates="questions")

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_public = Column(Boolean, default=False)  # Share with other users
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="notes")

class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)  # Percentage
    last_attempted = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress")
