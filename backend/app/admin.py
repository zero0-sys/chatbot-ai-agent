import pandas as pd
from pathlib import Path
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

ADMIN_TOKEN = "admin123"

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

def check_token(token: str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/admin")
def admin_dashboard(request: Request, token: str):
    check_token(token)

    suggest_file = DATA_DIR / "suggestions.csv"

    if suggest_file.exists():
        df = pd.read_csv(suggest_file)
        if "question" not in df.columns or "answer" not in df.columns:
            df = pd.DataFrame(columns=["question", "answer"])
    else:
        df = pd.DataFrame(columns=["question", "answer"])

    rows = [
        {"index": i, "question": r["question"], "answer": r["answer"]}
        for i, r in df.iterrows()
    ]

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "rows": rows,
            "token": token
        }
    )
