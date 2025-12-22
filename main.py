from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class Message(BaseModel):
    text: str


messages = []


@app.get("/hello")
def get_hello():
    return {"message": "Hello, from trackster, Arnold!"}


@app.post("/message")
def post_message(msg: Message):
    message_data = {"text": msg.text, "timestamp": datetime.now().isoformat()}
    messages.append(message_data)
    return {
        "received": msg.text,
        "timestamp": message_data["timestamp"],
        "total_messages": len(messages),
    }


@app.get("/messages")
def get_messages():
    return {"messages": messages}
