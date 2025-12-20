from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class Message(BaseModel):
    text: str


messages = []


@app.get("/hello")
def get_hello():
    return {"message": "Hello, Arnold!"}


@app.post("/message")
def post_message(msg: Message):
    messages.append(msg.text)
    return {"received": msg.text, "total_messages": len(messages)}


@app.get("/messages")
def get_messages():
    return {"messages": messages}
