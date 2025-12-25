import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "training_all.csv"

INTENTS = {
    "aku capek": [
        "aku capek",
        "capek banget",
        "gue capek",
        "kepala berat",
        "badan lelah"
    ],
    "aku lelah": [
        "aku lelah",
        "gue lelah",
        "lagi capek",
        "capek parah"
    ]
}

RESPONSES = {
    "aku capek": [
        "Istirahat dulu ya.",
        "Kayaknya kamu butuh rehat."
    ],
    "aku lelah": [
        "Istirahat dulu ya.",
        "Tubuh kamu minta berhenti sebentar."
    ]
}

rows = []

for intent, questions in INTENTS.items():
    answers = " | ".join(RESPONSES[intent])
    for q in questions:
        rows.append([q, answers])

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["question", "answer"])
    writer.writerows(rows)

print("✅ training.csv berhasil digenerate")
print(f"📄 Lokasi: {OUTPUT_FILE}")
print(f"🔢 Total data: {len(rows)}")
