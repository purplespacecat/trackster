from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, NoteDB

app = FastAPI()


class Note(BaseModel):
    text: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
