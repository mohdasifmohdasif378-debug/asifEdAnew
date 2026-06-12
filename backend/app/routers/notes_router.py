from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.models import User, Note
from app.schemas import NoteCreate, NoteUpdate, NoteResponse
from app.database import get_db

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("", response_model=NoteResponse, status_code=201)
async def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new note for the current user."""
    db_note = Note(
        user_id=current_user.id,
        title=note.title,
        content=note.content,
        topic_id=note.topic_id,
        is_public=note.is_public
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("", response_model=list[NoteResponse])
async def get_user_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all notes for the current user."""
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific note (only if owned by current user or public)."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(404, detail="Note not found")
    
    if note.user_id != current_user.id and not note.is_public:
        raise HTTPException(403, detail="Not authorized to view this note")
    
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a note (only if owned by current user)."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(404, detail="Note not found")
    
    if note.user_id != current_user.id:
        raise HTTPException(403, detail="Not authorized to update this note")
    
    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content
    if note_update.is_public is not None:
        note.is_public = note_update.is_public
    
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a note (only if owned by current user)."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(404, detail="Note not found")
    
    if note.user_id != current_user.id:
        raise HTTPException(403, detail="Not authorized to delete this note")
    
    db.delete(note)
    db.commit()

@router.get("/public/all", response_model=list[NoteResponse])
async def get_public_notes(db: Session = Depends(get_db)):
    """Get all public notes from all users."""
    public_notes = db.query(Note).filter(Note.is_public == True).limit(100).all()
    return public_notes
