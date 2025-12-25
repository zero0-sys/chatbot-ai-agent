from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model import SimpleChatModel

app = FastAPI(title="Matrix Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = SimpleChatModel("data/training.csv")

class ChatRequest(BaseModel):
    message: str
    userId: str | None = None

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    reply = model.predict(req.message)
    return {"reply": reply}
