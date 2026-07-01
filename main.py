from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from agent import handle_chat

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/")
def root():
    return {
        "message": "SHL Recommender API is live.",
        "health_check": "/health",
        "api_docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    result = handle_chat([m.dict() for m in request.messages])
    return result