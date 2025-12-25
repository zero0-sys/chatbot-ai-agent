import pandas as pd
from pathlib import Path
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pandas.errors import EmptyDataError

# ===============================
# CONFIG
# ===============================
ADMIN_TOKEN = "admin123"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"

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

def load_suggestions_df():
    """
    Load suggestions.csv safely.
    Return empty DataFrame if file missing or empty.
    """
    if not SUGGEST_FILE.exists():
        return pd.DataFrame(columns=["question", "answer"])

    try:
        df = pd.read_csv(SUGGEST_FILE)
    except EmptyDataError:
        return pd.DataFrame(columns=["question", "answer"])

    # pastikan kolom benar
    if "question" not in df.columns or "answer" not in df.columns:
        return pd.DataFrame(columns=["question", "answer"])

    return df

# ===============================
# DASHBOARD
# ===============================
@router.get("/admin")
def admin_dashboard(request: Request, token: str):
    check_token(token)

    df = load_suggestions_df()

    # PENTING: pakai row_id sendiri (bukan index pandas)
    rows = [
        {
            "row_id": i,
            "question": r["question"],
            "answer": r["answer"]
        }
        for i, r in enumerate(df.to_dict("records"))
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
def approve(row_id: int = Form(...), token: str = Form(...)):
    check_token(token)

    df_sug = load_suggestions_df()

    # kalau kosong, langsung balik
    if df_sug.empty:
        return RedirectResponse(f"/admin?token={token}", status_code=303)

    # ambil baris BERDASARKAN POSISI
    row = df_sug.iloc[row_id]

    # load training
    if TRAIN_FILE.exists():
        df_train = pd.read_csv(TRAIN_FILE)
    else:
        df_train = pd.DataFrame(columns=["question", "answer"])

    # append ke training
    df_train = pd.concat(
        [df_train, pd.DataFrame([row])],
        ignore_index=True
    )
    df_train.to_csv(TRAIN_FILE, index=False, quoting=1)

    # hapus dari suggestions berdasarkan posisi
    df_sug = df_sug.drop(df_sug.index[row_id])
    df_sug.to_csv(SUGGEST_FILE, index=False, quoting=1)

    return RedirectResponse(f"/admin?token={token}", status_code=303)

# ===============================
# REJECT
# ===============================
@router.post("/admin/reject")
def reject(row_id: int = Form(...), token: str = Form(...)):
    check_token(token)

    df_sug = load_suggestions_df()

    if not df_sug.empty:
        df_sug = df_sug.drop(df_sug.index[row_id])
        df_sug.to_csv(SUGGEST_FILE, index=False, quoting=1)

    return RedirectResponse(f"/admin?token={token}", status_code=303)
