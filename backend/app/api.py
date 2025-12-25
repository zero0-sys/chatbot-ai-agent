import csv
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel

from app.model import ChatModel
from app.text_utils import normalize

# ===============================
# PATH SETUP
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TRAIN_FILE = DATA_DIR / "training_all.csv"
SUGGEST_FILE = DATA_DIR / "suggestions.csv"
CONV_FILE = DATA_DIR / "conversations.csv"

DATA_DIR.mkdir(exist_ok=True)

# ===============================
# MODEL INIT
# ===============================
model = ChatModel(str(TRAIN_FILE))

# ===============================
# ROUTER
# ===============================
router = APIRouter()

# ===============================
# REQUEST SCHEMA
# ===============================
class ChatRequest(BaseModel):
    message: str
    userId: str | None = None


# ===============================
# HELPERS
# ===============================
def log_conversation(user_text: str, bot_reply: str):
    new_file = not CONV_FILE.exists()

    with open(CONV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        if new_file:
            writer.writerow(["time", "user", "bot"])

        writer.writerow([
            datetime.now().isoformat(),
            user_text,
            bot_reply
        ])


def save_suggestion(question: str, answer: str):
    new_file = not SUGGEST_FILE.exists()

    with open(SUGGEST_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        if new_file:
            writer.writerow(["question", "answer"])

        writer.writerow([
            normalize(question),
            answer
        ])


# ===============================
# CHAT ENDPOINT
# ===============================
@router.post("/chat")
def chat(req: ChatRequest):
    user_text = req.message.strip()

    if not user_text:
        return {"reply": "Kamu belum ngetik apa-apa."}

    # =========================
    # MODEL PREDICT
    # =========================
    reply, confidence = model.predict(user_text)

    # =========================
    # LOG SEMUA CHAT
    # =========================
    log_conversation(user_text, reply)

    # =========================
    # AUTO LEARNING (PENDING)
    # =========================
    if confidence < 1:
        save_suggestion(user_text, reply)

    return {
        "reply": reply,
        "confidence": confidence
    }
