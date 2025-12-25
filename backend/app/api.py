from fastapi import APIRouter
from pydantic import BaseModel
from app.model import ChatModel
import csv
from datetime import datetime

LOG_FILE = "data/conversations.csv"

def log_conversation(user_text, bot_reply):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow([
            datetime.now().isoformat(),
            user_text,
            bot_reply
        ])

router = APIRouter()
model = ChatModel("data/training_all.csv")

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    return {"reply": model.predict(req.message)}
