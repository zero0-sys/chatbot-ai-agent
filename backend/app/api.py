import re
import csv
import math
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel

from app.model import ChatModel
from app.text_utils import normalize

# ===============================
# PATH
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

TRAIN_FILE = DATA_DIR / "training_all.csv"
SUGGEST_FILE = DATA_DIR / "suggestions.csv"
CONV_FILE = DATA_DIR / "conversations.csv"

# ===============================
# MODEL
# ===============================
model = ChatModel(str(TRAIN_FILE))
router = APIRouter()

# ===============================
# REQUEST
# ===============================
class ChatRequest(BaseModel):
    message: str
    userId: str | None = None

# ===============================
# LOGGING
# ===============================
def log_conversation(user_text, bot_reply):
    new = not CONV_FILE.exists()
    with open(CONV_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "user", "bot"])
        w.writerow([datetime.now().isoformat(), user_text, bot_reply])

def save_suggestion(q, a):
    new = not SUGGEST_FILE.exists()
    with open(SUGGEST_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["question", "answer"])
        w.writerow([normalize(q), a])

# ===============================
# MATEMATIKA
# ===============================
def solve_geometry(text):
    t = text.lower()
    nums = list(map(float, re.findall(r"\d+", t)))

    if "luas segitiga" in t and len(nums) >= 2:
        a, h = nums[0], nums[1]
        return f"Luas segitiga = 1/2 x alas x tinggi = {0.5*a*h}"

    if "luas persegi" in t and nums:
        s = nums[0]
        return f"Luas persegi = {s*s}"

    return None

def solve_algebra(text):
    t = text.replace(" ", "").lower()
    m = re.match(r"([0-9]*)x([\+\-][0-9]+)?=([0-9]+)", t)
    if not m:
        return None
    a = int(m.group(1)) if m.group(1) else 1
    b = int(m.group(2)) if m.group(2) else 0
    c = int(m.group(3))
    x = (c - b) / a
    return f"x = {x}"

def solve_calculus(text):
    t = text.replace(" ", "").lower()
    if t in ["turunanx2", "turunanx^2"]:
        return "d/dx x² = 2x"
    if t in ["integralx"]:
        return "∫ x dx = 1/2 x² + C"
    return None

# ===============================
# CODE GENERATOR
# ===============================
def generate_code(text: str):
    t = text.lower()

    # === HELLO WORLD ===
    if "hello world" in t:
        if "python" in t:
            return "print('Hello World')"
        if "javascript" in t:
            return "console.log('Hello World');"
        if "java" in t:
            return (
                "public class Main {\n"
                "  public static void main(String[] args) {\n"
                "    System.out.println(\"Hello World\");\n"
                "  }\n"
                "}"
            )

    # === FAKTORIAL ===
    if "faktorial" in t:
        if "python" in t:
            return (
                "def faktorial(n):\n"
                "    if n == 0:\n"
                "        return 1\n"
                "    return n * faktorial(n-1)\n"
            )

        if "javascript" in t:
            return (
                "function faktorial(n) {\n"
                "  if (n === 0) return 1;\n"
                "  return n * faktorial(n - 1);\n"
                "}"
            )

    # === FIBONACCI ===
    if "fibonacci" in t:
        if "python" in t:
            return (
                "def fibonacci(n):\n"
                "    a, b = 0, 1\n"
                "    for _ in range(n):\n"
                "        a, b = b, a + b\n"
                "    return a\n"
            )

    # === IF ELSE ===
    if "if else" in t:
        if "python" in t:
            return (
                "if kondisi:\n"
                "    print('Benar')\n"
                "else:\n"
                "    print('Salah')\n"
            )

    return None

def generate_frontend_code(text: str):
    t = text.lower()

    # =========================
    # LANDING PAGE
    # =========================
    if "landing page" in t:
        return (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            "  <title>Landing Page</title>\n"
            "  <style>\n"
            "    body { font-family: Arial; text-align: center; padding: 50px; }\n"
            "    button { padding: 10px 20px; background: black; color: white; border: none; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <h1>Selamat Datang</h1>\n"
            "  <p>Ini landing page sederhana</p>\n"
            "  <button>Mulai</button>\n"
            "</body>\n"
            "</html>"
        )

    # =========================
    # FORM LOGIN
    # =========================
    if "form login" in t:
        return (
            "<form>\n"
            "  <h2>Login</h2>\n"
            "  <input type='text' placeholder='Username'><br><br>\n"
            "  <input type='password' placeholder='Password'><br><br>\n"
            "  <button>Login</button>\n"
            "</form>"
        )

    # =========================
    # BUTTON + JS
    # =========================
    if "button alert" in t or "tombol alert" in t:
        return (
            "<button onclick='showAlert()'>Klik</button>\n"
            "<script>\n"
            "function showAlert() {\n"
            "  alert('Tombol diklik');\n"
            "}\n"
            "</script>"
        )

    # =========================
    # NAVBAR
    # =========================
    if "navbar" in t:
        return (
            "<nav style='background:black;padding:10px;'>\n"
            "  <a href='#' style='color:white;margin:10px;'>Home</a>\n"
            "  <a href='#' style='color:white;margin:10px;'>About</a>\n"
            "  <a href='#' style='color:white;margin:10px;'>Contact</a>\n"
            "</nav>"
        )

    # =========================
    # FETCH API
    # =========================
    if "fetch api" in t:
        return (
            "<script>\n"
            "fetch('https://api.example.com/data')\n"
            "  .then(res => res.json())\n"
            "  .then(data => console.log(data));\n"
            "</script>"
        )

    return None

# ===============================
# CHAT ENDPOINT
# ===============================
@router.post("/chat")
def chat(req: ChatRequest):
    user_text = req.message.strip()

    if not user_text:
        return {"reply": "Kamu belum ngetik apa apa."}

    frontend = generate_frontend_code(user_text)
    if frontend:
        log_conversation(user_text, frontend)
        return {"reply": frontend}

    # === CODE GENERATOR ===
    code = generate_code(user_text)
    if code:
        log_conversation(user_text, code)
        return {"reply": code}

    # === GEOMETRI ===
    geo = solve_geometry(user_text)
    if geo:
        log_conversation(user_text, geo)
        return {"reply": geo}

    # === ALJABAR ===
    alg = solve_algebra(user_text)
    if alg:
        log_conversation(user_text, alg)
        return {"reply": alg}

    # === KALKULUS ===
    calc = solve_calculus(user_text)
    if calc:
        log_conversation(user_text, calc)
        return {"reply": calc}

    # === CHAT NORMAL ===
    reply, confidence = model.predict(user_text)
    log_conversation(user_text, reply)

    if confidence < 1:
        save_suggestion(user_text, reply)

    return {
        "reply": reply,
        "confidence": confidence
    }
