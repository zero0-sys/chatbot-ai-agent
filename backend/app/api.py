from fastapi import APIRouter
from pydantic import BaseModel
from app.model import ChatModel
import csv
from datetime import datetime
import csv
from pathlib import Path
from app.text_utils import normalize

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SUGGEST_FILE = DATA_DIR / "suggestions.csv"

def save_suggestion(question: str, answer: str):
    DATA_DIR.mkdir(exist_ok=True)

    is_new = not SUGGEST_FILE.exists()

    with open(SUGGEST_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        if is_new:
            writer.writerow(["question", "answer"])

        writer.writerow([
            normalize(question),
            answer
        ])

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
