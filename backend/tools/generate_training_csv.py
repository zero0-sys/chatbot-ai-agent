import csv
import random

OUTPUT_FILE = "training.csv"

INTENTS = {
    "capek": {
        "questions": [
            "aku capek",
            "capek banget",
            "badan pegel",
            "energi habis",
            "aku kecapekan",
            "cape seharian",
            "capek mental",
            "kepala berat"
        ],
        "answers": [
            "Istirahat dulu ya|Tubuh kamu butuh jeda",
            "Kayaknya kamu perlu rehat|Jangan dipaksain",
            "Capek itu wajar|Tarik napas dulu"
        ]
    },

    "sedih": {
        "questions": [
            "aku sedih",
            "pengen nangis",
            "hati berat",
            "aku down",
            "aku kecewa",
            "ngerasa gagal",
            "kosong banget"
        ],
        "answers": [
            "Aku dengerin kamu|Nggak apa-apa ngerasa gini",
            "Kedengerannya berat|Aku temenin",
            "Perasaan kamu valid|Pelan-pelan ya"
        ]
    },

    "bercanda": {
        "questions": [
            "wkwk",
            "haha",
            "lol",
            "ngakak",
            "receh banget",
            "random anjir",
            "ga jelas"
        ],
        "answers": [
            "Wkwk|Aku juga bingung",
            "Haha|Nggak ngerti tapi lucu",
            "Lah iya|Aneh tapi yaudah"
        ]
    },

    "pintar": {
        "questions": [
            "apa itu fotosintesis",
            "kenapa langit biru",
            "siapa einstein",
            "apa itu ai",
            "kenapa manusia butuh tidur",
            "apa itu internet"
        ],
        "answers": [
            "Itu proses ilmiah|Aku jelasin singkat ya",
            "Ada penjelasan sainsnya|Mau versi gampang atau detail",
            "Ini topik menarik|Aku coba jelasin pelan"
        ]
    }
}

def generate_rows(total=500):
    rows = []
    intents = list(INTENTS.keys())

    while len(rows) < total:
        intent = random.choice(intents)
        q = random.choice(INTENTS[intent]["questions"])
        a = random.choice(INTENTS[intent]["answers"])
        rows.append([q, a])

    return rows

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(
        f,
        delimiter=",",
        quotechar=None,
        quoting=csv.QUOTE_NONE,
        escapechar="\\"
    )

    writer.writerow(["question", "answer"])

    for row in generate_rows(500):
        writer.writerow(row)

print("✅ training.csv berhasil dibuat TANPA tanda petik")
print("   total baris:", 500)