#!/usr/bin/env python3
"""
Seed Database with Exam Content
Populates ExamBrain database with UPSC, SSC, NDA, Banking exams
and their comprehensive syllabus and sample questions
"""

import os
import sys
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import Base, Exam, Subject, Topic, Question

def seed_database():
    """Seed the database with comprehensive exam content."""
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_exams = db.query(Exam).first()
        if existing_exams:
            print("✅ Database already seeded. Skipping.")
            return
        
        print("🌱 Seeding database with exam content...")
        
        # ===== UPSC CONTENT =====
        print("\n📚 Adding UPSC Content...")
        upsc = Exam(
            name="UPSC",
            description="Union Public Service Commission - Civil Services Examination"
        )
        db.add(upsc)
        db.flush()
        
        upsc_subjects = {
            "General Studies I (History, Culture, Geography, Environment)": {
                "weightage": 20,
                "topics": [
                    ("Ancient India", 3, "Ancient history, Mauryan, Gupta empires"),
                    ("Medieval India", 3, "Muslim kingdoms, Mughal empire"),
                    ("Modern India", 4, "British rule, Independence struggle, Constitution"),
                    ("World Geography", 3, "Physical, Political, Economic geography"),
                    ("Indian Geography", 4, "Physical features, Climate, Natural resources"),
                    ("Indian Culture", 3, "Art, Literature, Philosophy, Religion"),
                    ("Environment & Ecology", 2, "Biodiversity, Conservation, Climate change"),
                ]
            },
            "General Studies II (Polity, Social Issues, Governance)": {
                "weightage": 18,
                "topics": [
                    ("Constitution of India", 4, "Articles, Amendments, Fundamental Rights"),
                    ("Parliament & Executive", 3, "President, PM, Parliament structure"),
                    ("Judiciary", 2, "Supreme Court, High Courts, Judicial review"),
                    ("Elections & Political System", 2, "Election commission, Voting"),
                    ("Social Issues", 4, "Education, Health, Poverty, Gender"),
                    ("Welfare Schemes", 2, "Government schemes and policies"),
                    ("Human Rights", 1, "Constitutional safeguards"),
                ]
            },
            "General Studies III (Economy, Science, Technology, Security)": {
                "weightage": 19,
                "topics": [
                    ("Indian Economy", 4, "GDP, Inflation, Banking, Money market"),
                    ("Budget & Taxation", 2, "Union budget, Tax system, Fiscal policy"),
                    ("Agriculture", 2, "Crop production, Green revolution, Land reforms"),
                    ("Industry & Services", 1, "Manufacturing, Services sector"),
                    ("Science & Technology", 3, "Latest technology, Space, Biotechnology"),
                    ("Security & Defense", 2, "National security, Terrorism, Cyber threats"),
                    ("Environmental Issues", 2, "Pollution, Climate, Disasters"),
                ]
            },
            "General Studies IV (Ethics & Integrity)": {
                "weightage": 8,
                "topics": [
                    ("Ethical concepts", 2, "Right, Wrong, Duty, Virtue"),
                    ("Decision making", 2, "Ethical dilemmas, Problem solving"),
                    ("Public service ethics", 2, "Governance, Corruption"),
                    ("Case studies", 2, "Real-world ethical scenarios"),
                ]
            }
        }
        
        for subject_name, data in upsc_subjects.items():
            subject = Subject(
                exam_id=upsc.id,
                name=subject_name,
                weightage=data["weightage"],
                description=f"UPSC {subject_name}"
            )
            db.add(subject)
            db.flush()
            
            for topic_name, wt, desc in data["topics"]:
                topic = Topic(
                    exam_id=upsc.id,
                    subject_id=subject.id,
                    name=topic_name,
                    description=desc,
                    weightage=wt,
                    difficulty="medium"
                )
                db.add(topic)
        
        db.commit()
        print("✅ UPSC content added")
        
        # ===== SSC CONTENT =====
        print("\n📚 Adding SSC Content...")
        ssc = Exam(
            name="SSC",
            description="Staff Selection Commission - CHSL, CGL, MTS Exams"
        )
        db.add(ssc)
        db.flush()
        
        ssc_subjects = {
            "English Language": {
                "weightage": 25,
                "topics": [
                    ("Reading Comprehension", 5, "Passage comprehension, vocabulary"),
                    ("Grammar", 5, "Tenses, Clauses, Articles, Prepositions"),
                    ("Vocabulary", 4, "Synonyms, Antonyms, Words"),
                    ("Sentence Correction", 3, "Error detection, Rearrangement"),
                    ("Writing", 4, "Spotting errors, Para jumbles"),
                    ("Idioms & Phrases", 3, "Common expressions and meanings"),
                ]
            },
            "Quantitative Aptitude": {
                "weightage": 25,
                "topics": [
                    ("Number System", 3, "Prime, composite, divisibility"),
                    ("Percentage", 3, "Profit-loss, discount, SI-CI"),
                    ("Speed & Distance", 2, "Trains, boats, motion"),
                    ("Ratio & Proportion", 2, "Partnership, mixtures"),
                    ("Algebra", 4, "Quadratic equations, surds"),
                    ("Geometry", 3, "Triangles, circles, area, volume"),
                    ("Data Interpretation", 3, "Tables, graphs, pie charts"),
                    ("Trigonometry", 2, "Ratios, heights and distances"),
                ]
            },
            "Reasoning": {
                "weightage": 25,
                "topics": [
                    ("Analogy", 3, "Word analogies, number patterns"),
                    ("Classification", 3, "Odd one out, grouping"),
                    ("Series", 3, "Number series, alphabet series"),
                    ("Coding-Decoding", 2, "Letter/number codes, patterns"),
                    ("Direction Sense", 2, "Directions, paths"),
                    ("Blood Relations", 2, "Family connections"),
                    ("Syllogism", 2, "Logical conclusions"),
                    ("Puzzles", 3, "Logic puzzles, arrangements"),
                ]
            },
            "General Awareness": {
                "weightage": 25,
                "topics": [
                    ("Current Affairs", 4, "National & international news"),
                    ("History", 3, "India independence, freedom fighters"),
                    ("Geography", 2, "Indian states, capitals, monuments"),
                    ("Polity", 2, "Constitution, Government"),
                    ("Science", 3, "Physics, Chemistry, Biology basics"),
                    ("Economics", 2, "Banking, RBI, Economy"),
                    ("Sports", 2, "National & international sports"),
                    ("Culture", 1, "Indian festivals, heritage"),
                ]
            }
        }
        
        for subject_name, data in ssc_subjects.items():
            subject = Subject(
                exam_id=ssc.id,
                name=subject_name,
                weightage=data["weightage"],
                description=f"SSC {subject_name}"
            )
            db.add(subject)
            db.flush()
            
            for topic_name, wt, desc in data["topics"]:
                topic = Topic(
                    exam_id=ssc.id,
                    subject_id=subject.id,
                    name=topic_name,
                    description=desc,
                    weightage=wt,
                    difficulty="easy"  # SSC is generally easier
                )
                db.add(topic)
        
        db.commit()
        print("✅ SSC content added")
        
        # ===== NDA CONTENT =====
        print("\n📚 Adding NDA Content...")
        nda = Exam(
            name="NDA",
            description="National Defence Academy - Military Academy Selection Exam"
        )
        db.add(nda)
        db.flush()
        
        nda_subjects = {
            "Mathematics": {
                "weightage": 33,
                "topics": [
                    ("Algebra", 4, "Sets, Relations, Quadratic equations"),
                    ("Trigonometry", 3, "Ratios, identities, solutions"),
                    ("Geometry", 4, "Coordinates, Circles, Lines"),
                    ("Statistics", 3, "Mean, variance, probability"),
                    ("Calculus", 3, "Limits, Derivatives, Integrals"),
                    ("Vectors", 3, "Addition, Dot product, Cross product"),
                    ("Numbers", 2, "Permutations, Combinations"),
                ]
            },
            "General Knowledge": {
                "weightage": 33,
                "topics": [
                    ("History", 3, "Ancient, Medieval, Modern India"),
                    ("Geography", 3, "Physical, Political, Economic"),
                    ("Polity", 2, "Constitution, Government"),
                    ("Science", 4, "Physics, Chemistry, Biology"),
                    ("Defence", 4, "Armed forces, Security"),
                    ("Current Affairs", 3, "National & international events"),
                    ("Culture & Art", 2, "Indian heritage"),
                ]
            },
            "English": {
                "weightage": 34,
                "topics": [
                    ("Reading", 5, "Comprehension, vocabulary"),
                    ("Grammar", 5, "Tenses, Errors, Corrections"),
                    ("Writing", 4, "Essays, Letters"),
                    ("Verbal Ability", 4, "Analogies, Series, Logic"),
                    ("Antonyms & Synonyms", 3, "Word meanings"),
                    ("Sentence Arrangement", 3, "Jumbled sentences"),
                    ("Spotting Errors", 3, "Grammatical errors"),
                ]
            }
        }
        
        for subject_name, data in nda_subjects.items():
            subject = Subject(
                exam_id=nda.id,
                name=subject_name,
                weightage=data["weightage"],
                description=f"NDA {subject_name}"
            )
            db.add(subject)
            db.flush()
            
            for topic_name, wt, desc in data["topics"]:
                topic = Topic(
                    exam_id=nda.id,
                    subject_id=subject.id,
                    name=topic_name,
                    description=desc,
                    weightage=wt,
                    difficulty="hard"  # NDA is competitive
                )
                db.add(topic)
        
        db.commit()
        print("✅ NDA content added")
        
        # ===== BANKING CONTENT =====
        print("\n📚 Adding Banking Exam Content...")
        banking = Exam(
            name="Banking",
            description="Banking Exams - IBPS, SBI, RBI, NABARD"
        )
        db.add(banking)
        db.flush()
        
        banking_subjects = {
            "Banking Awareness": {
                "weightage": 15,
                "topics": [
                    ("Banking Basics", 2, "Types of banks, RBI, NABARD"),
                    ("Banking Regulations", 2, "KYC, AML, Compliance"),
                    ("Banking Products", 3, "Loans, Deposits, Insurance"),
                    ("Digital Banking", 2, "Online banking, Mobile banking"),
                    ("Recent Reforms", 3, "Demonetization, GST, Payment systems"),
                    ("International Banking", 2, "SWIFT, FOREX, International trade"),
                ]
            },
            "Quantitative Aptitude": {
                "weightage": 25,
                "topics": [
                    ("Simplification", 2, "BODMAS, Percentages"),
                    ("Number System", 2, "Divisibility, Prime numbers"),
                    ("SI & CI", 3, "Simple Interest, Compound Interest"),
                    ("Profit & Loss", 3, "Cost price, Selling price"),
                    ("Speed & Distance", 2, "Average, Trains"),
                    ("Algebra", 2, "Equations, Polynomials"),
                    ("Geometry", 2, "Area, Perimeter, Volume"),
                    ("Data Interpretation", 4, "Tables, Graphs, Caselets"),
                ]
            },
            "Reasoning": {
                "weightage": 25,
                "topics": [
                    ("Analogy", 2, "Word and number analogies"),
                    ("Classification", 2, "Grouping, Odd one out"),
                    ("Series", 2, "Number and letter series"),
                    ("Coding-Decoding", 2, "Symbols, Letters"),
                    ("Blood Relations", 2, "Family connections"),
                    ("Syllogism", 2, "Logical conclusions"),
                    ("Puzzles", 4, "Arrangement, Selection"),
                    ("Direction", 2, "Directions, Path"),
                ]
            },
            "English Language": {
                "weightage": 20,
                "topics": [
                    ("Reading", 3, "Comprehension, Passage"),
                    ("Grammar", 3, "Errors, Corrections"),
                    ("Vocabulary", 2, "Synonyms, Antonyms"),
                    ("Sentence Correction", 3, "Rearrangement, Fragments"),
                    ("Cloze Test", 2, "Fill in blanks"),
                    ("Para Jumbles", 2, "Sentence arrangement"),
                    ("Spotting Errors", 2, "Error detection"),
                    ("Phrases & Idioms", 1, "Common expressions"),
                ]
            },
            "General Awareness": {
                "weightage": 15,
                "topics": [
                    ("Banking & Economy", 3, "RBI, Banking system"),
                    ("Finance", 2, "Budget, Stock market"),
                    ("Current Affairs", 3, "Recent events"),
                    ("Static GK", 3, "History, Geography, Polity"),
                    ("Science & Tech", 2, "Recent innovations"),
                    ("Awards & Honors", 2, "National & international"),
                ]
            }
        }
        
        for subject_name, data in banking_subjects.items():
            subject = Subject(
                exam_id=banking.id,
                name=subject_name,
                weightage=data["weightage"],
                description=f"Banking {subject_name}"
            )
            db.add(subject)
            db.flush()
            
            for topic_name, wt, desc in data["topics"]:
                topic = Topic(
                    exam_id=banking.id,
                    subject_id=subject.id,
                    name=topic_name,
                    description=desc,
                    weightage=wt,
                    difficulty="medium"
                )
                db.add(topic)
        
        db.commit()
        print("✅ Banking content added")
        
        print("\n✨ Database seeding complete!")
        print("\n📊 Summary:")
        exams = db.query(Exam).all()
        for exam in exams:
            subjects = db.query(Subject).filter(Subject.exam_id == exam.id).count()
            topics = db.query(Topic).filter(Topic.exam_id == exam.id).count()
            print(f"  {exam.name}: {subjects} subjects, {topics} topics")
        
        print("\n💡 Next: Add specific questions using the API or admin panel")
        print("🌐 Access: http://localhost:3001")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
