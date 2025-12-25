import pandas as pd
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

ADMIN_TOKEN = "admin123"
SUGGEST_FILE = "data/suggestions.csv"
TRAIN_FILE = "data/training.csv"

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def check_token(token: str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/admin")
def admin_dashboard(request: Request, token: str):
    check_token(token)

    try:
        df = pd.read_csv(SUGGEST_FILE)
    except FileNotFoundError:
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

@router.post("/admin/approve")
def approve(index: int = Form(...), token: str = Form(...)):
    check_token(token)

    df_sug = pd.read_csv(SUGGEST_FILE)
    df_train = pd.read_csv(TRAIN_FILE)

    row = df_sug.iloc[index]
    df_train = pd.concat([df_train, row.to_frame().T], ignore_index=True)

    df_train.to_csv(TRAIN_FILE, index=False, quoting=1)
    df_sug = df_sug.drop(index)
    df_sug.to_csv(SUGGEST_FILE, index=False, quoting=1)

    return RedirectResponse(f"/admin?token={token}", status_code=303)

@router.post("/admin/reject")
def reject(index: int = Form(...), token: str = Form(...)):
    check_token(token)

    df_sug = pd.read_csv(SUGGEST_FILE)
    df_sug = df_sug.drop(index)
    df_sug.to_csv(SUGGEST_FILE, index=False, quoting=1)

    return RedirectResponse(f"/admin?token={token}", status_code=303)
