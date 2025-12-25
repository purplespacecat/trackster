from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, MessageDB

app = FastAPI()


class Message(BaseModel):
    text: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# messages = []


@app.get("/hello")
def get_hello():
    return {"message": "Hello, from trackster, Arnold!"}


@app.post("/message")
def post_message(msg: Message, db: Session = Depends(get_db)):
    # message_data = {"text": msg.text, "timestamp": datetime.now().isoformat()}
    # messages.append(message_data)
    # Create new message in database
    db_message = MessageDB(text=msg.text, timestamp=datetime.now())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # Get total count
    total = db.query(MessageDB).count()

    return {
        "received": msg.text,
        "timestamp": db_message.timestamp.isoformat(),
        "total_messages": total,
    }


@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    db_messages = db.query(MessageDB).order_by(MessageDB.timestamp).all()
    messages = [
        {"id": msg.id, "text": msg.text, "timestamp": msg.timestamp.isoformat()}
        for msg in db_messages
    ]
    return {"messages": messages}


@app.delete("/message/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
        return {"success": True, "message": "Message deleted"}
    return {"success": False, "message": "Message not found"}
