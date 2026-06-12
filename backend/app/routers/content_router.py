from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Question, Topic, Subject, Exam
from app.schemas import QuestionResponse, TopicResponse, SubjectResponse, ExamResponse
from app.database import get_db
from typing import Optional

router = APIRouter(prefix="/content", tags=["Exam Content"])

@router.get("/exams", response_model=list[ExamResponse])
async def get_exams(db: Session = Depends(get_db)):
    """Get all available exams."""
    exams = db.query(Exam).all()
    return exams

@router.get("/exams/{exam_id}/subjects", response_model=list[SubjectResponse])
async def get_subjects(exam_id: int, db: Session = Depends(get_db)):
    """Get subjects for a specific exam."""
    subjects = db.query(Subject).filter(Subject.exam_id == exam_id).all()
    if not subjects:
        raise HTTPException(404, detail="No subjects found for this exam")
    return subjects

@router.get("/subjects/{subject_id}/topics", response_model=list[TopicResponse])
async def get_topics(subject_id: int, db: Session = Depends(get_db)):
    """Get topics for a specific subject."""
    topics = db.query(Topic).filter(Topic.subject_id == subject_id).all()
    if not topics:
        raise HTTPException(404, detail="No topics found for this subject")
    return topics

@router.get("/topics/{topic_id}/questions", response_model=list[QuestionResponse])
async def get_questions_by_topic(
    topic_id: int,
    limit: Optional[int] = 50,
    db: Session = Depends(get_db)
):
    """Get questions for a specific topic (answers hidden)."""
    if limit and limit > 1000:
        limit = 1000
    
    questions = db.query(Question).filter(Question.topic_id == topic_id).limit(limit).all()
    if not questions:
        raise HTTPException(404, detail="No questions found for this topic")
    return questions

@router.get("/topics/{topic_id}/questions/{question_id}", response_model=QuestionResponse)
async def get_question(
    topic_id: int,
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific question (answer hidden)."""
    question = db.query(Question).filter(
        Question.id == question_id,
        Question.topic_id == topic_id
    ).first()
    if not question:
        raise HTTPException(404, detail="Question not found")
    return question

@router.get("/search/questions")
async def search_questions(
    exam_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    limit: Optional[int] = 50,
    db: Session = Depends(get_db)
):
    """Search questions with filters."""
    query = db.query(Question)
    
    if exam_id:
        query = query.filter(Question.exam_id == exam_id)
    if subject_id:
        query = query.join(Topic).filter(Topic.subject_id == subject_id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    
    if limit and limit > 1000:
        limit = 1000
    
    questions = query.limit(limit).all()
    return questions

@router.get("/syllabus/{exam_id}")
async def get_syllabus(exam_id: int, db: Session = Depends(get_db)):
    """Get complete syllabus for an exam with topics and weightage."""
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(404, detail="Exam not found")
    
    subjects = db.query(Subject).filter(Subject.exam_id == exam_id).all()
    
    syllabus = {
        "exam": exam.name,
        "subjects": []
    }
    
    for subject in subjects:
        topics = db.query(Topic).filter(Topic.subject_id == subject.id).all()
        subject_data = {
            "name": subject.name,
            "weightage": subject.weightage,
            "description": subject.description,
            "topics": [
                {
                    "name": topic.name,
                    "weightage": topic.weightage,
                    "difficulty": topic.difficulty,
                    "description": topic.description
                }
                for topic in topics
            ]
        }
        syllabus["subjects"].append(subject_data)
    
    return syllabus

@router.get("/stats/exam/{exam_id}")
async def get_exam_stats(exam_id: int, db: Session = Depends(get_db)):
    """Get statistics about questions in an exam."""
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(404, detail="Exam not found")
    
    total_questions = db.query(Question).filter(Question.exam_id == exam_id).count()
    subjects = db.query(Subject).filter(Subject.exam_id == exam_id).count()
    topics = db.query(Topic).filter(Topic.exam_id == exam_id).count()
    
    difficulty_stats = db.query(
        Question.difficulty,
        db.func.count(Question.id).label("count")
    ).filter(Question.exam_id == exam_id).group_by(Question.difficulty).all()
    
    return {
        "exam_name": exam.name,
        "total_questions": total_questions,
        "total_subjects": subjects,
        "total_topics": topics,
        "difficulty_distribution": [
            {"difficulty": d, "count": c} for d, c in difficulty_stats
        ]
    }
