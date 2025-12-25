import csv
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
DATA_DIR.mkdir(exist_ok=True)

SUGGEST_FILE = DATA_DIR / "suggestions.csv"

# ===============================
# MODEL INIT
# ===============================
model = ChatModel(DATA_DIR / "training_all.csv")

router = APIRouter()

# ===============================
# REQUEST SCHEMA
# ===============================
class ChatRequest(BaseModel):
    message: str

# ===============================
# HELPER: SAVE SUGGESTION
# ===============================
def save_suggestion(question: str, answer: str):
    is_new = not SUGGEST_FILE.exists()

    with open(SUGGEST_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        # tulis header kalau file baru
        if is_new:
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
    reply, confidence = model.predict(req.message)

    # confidence RENDAH → MASUK SUGGESTION
    if confidence < 1:
        save_suggestion(req.message, reply)

    return {
        "reply": reply,
        "confidence": confidence
    }
