import csv
import pandas as pd
from app.text_utils import normalize

TRAIN_FILE = "data/training.csv"
LOG_FILE = "data/conversations.csv"
OUT_FILE = "data/suggestions.csv"

df_train = pd.read_csv(TRAIN_FILE)
existing = set(df_train["question"].str.lower())

suggestions = []

with open(LOG_FILE, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for _, user_text, bot_reply in reader:
        q = normalize(user_text)

        # hanya sarankan kalau BELUM ADA di training
        if q not in existing and len(q.split()) <= 4:
            suggestions.append([q, bot_reply])
            existing.add(q)

if suggestions:
    pd.DataFrame(
        suggestions,
        columns=["question", "answer"]
    ).to_csv(OUT_FILE, index=False, quoting=1)

    print(f"✅ {len(suggestions)} saran training dibuat")
else:
    print("ℹ️ Tidak ada saran baru")
