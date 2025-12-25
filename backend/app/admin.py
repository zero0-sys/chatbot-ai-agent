import pandas as pd
from pathlib import Path
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

# ===============================
# CONFIG
# ===============================
ADMIN_TOKEN = "admin123"

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"

SUGGEST_FILE = DATA_DIR / "suggestions.csv"
TRAIN_FILE = DATA_DIR / "training_all.csv"

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# ===============================
# HELPERS
# ===============================
def check_token(token: str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ===============================
# DASHBOARD
# ===============================
@router.get("/admin")
def admin_dashboard(request: Request, token: str):
    check_token(token)

    if SUGGEST_FILE.exists():
        df = pd.read_csv(SUGGEST_FILE)
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

# ===============================
# APPROVE
# ===============================
@router.post("/admin/approve")
def approve(index: int = Form(...), token: str = Form(...)):
    check_token(token)

    df_sug = pd.read_csv(SUGGEST_FILE)
    df_train = pd.read_csv(TRAIN_FILE)

    row = df_sug.iloc[index]
    df_train = pd.concat([df_train, row.to_frame().T], ignore_index=True)

    df_train.to_csv(TRAIN_FILE, index=False, quoting=1)
    df_sug.drop(index).to_csv(SUGGEST_FILE, index=False, quoting=1)

    return RedirectResponse(
        url=f"/admin?token={token}",
        status_code=303
    )

# ===============================
# REJECT
# ===============================
@router.post("/admin/reject")
def reject(index: int = Form(...), token: str = Form(...)):
    check_token(token)

    df_sug = pd.read_csv(SUGGEST_FILE)
    df_sug.drop(index).to_csv(SUGGEST_FILE, index=False, quoting=1)

    return RedirectResponse(
        url=f"/admin?token={token}",
        status_code=303
    )
