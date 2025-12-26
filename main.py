from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, NoteDB, SummaryDB
from ai_service import generate_notes_summary

app = FastAPI()


class Note(BaseModel):
    text: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Global exception handlers
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"success": False, "detail": "Database operation failed"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "detail": "An unexpected error occurred"}
    )


@app.get("/hello")
def get_hello():
    return {"message": "Hello, from trackster!"}


@app.post("/note")
def post_note(note: Note, db: Session = Depends(get_db)):
    # Create new note in database
    db_note = NoteDB(text=note.text, timestamp=datetime.now())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    # Get total count
    total = db.query(NoteDB).count()

    return {
        "received": note.text,
        "timestamp": db_note.timestamp.isoformat(),
        "total_notes": total,
    }


@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    db_notes = db.query(NoteDB).order_by(NoteDB.timestamp).all()
    notes = [
        {"id": note.id, "text": note.text, "timestamp": note.timestamp.isoformat()}
        for note in db_notes
    ]
    return {"notes": notes}


@app.delete("/note/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return {"success": True, "message": "Note deleted"}
    return {"success": False, "message": "Note not found"}


@app.post("/notes/summary")
def create_summary(count: int = 6, db: Session = Depends(get_db)):
    """Generate an AI summary of the last N notes"""
    # Get the last N notes
    db_notes = db.query(NoteDB).order_by(NoteDB.timestamp.desc()).limit(count).all()

    if not db_notes:
        return {"success": False, "message": "No notes available to summarize"}

    # Prepare notes for AI
    notes_for_ai = [
        {"text": note.text, "timestamp": note.timestamp.isoformat()}
        for note in reversed(db_notes)  # Reverse to chronological order
    ]

    # Generate summary using AI
    summary_text = generate_notes_summary(notes_for_ai, count)

    # Save summary to database
    db_summary = SummaryDB(
        summary_text=summary_text,
        note_count=len(db_notes),
        timestamp=datetime.now()
    )
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)

    return {
        "success": True,
        "summary": {
            "id": db_summary.id,
            "text": db_summary.summary_text,
            "note_count": db_summary.note_count,
            "timestamp": db_summary.timestamp.isoformat()
        }
    }


@app.get("/notes/summary/latest")
def get_latest_summary(db: Session = Depends(get_db)):
    """Get the most recent summary from the database"""
    db_summary = db.query(SummaryDB).order_by(SummaryDB.timestamp.desc()).first()

    if not db_summary:
        return {"success": False, "message": "No summaries generated yet"}

    return {
        "success": True,
        "summary": {
            "id": db_summary.id,
            "text": db_summary.summary_text,
            "note_count": db_summary.note_count,
            "timestamp": db_summary.timestamp.isoformat()
        }
    }
