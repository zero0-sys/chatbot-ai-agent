import re

STOPWORDS = {
    "aku", "kamu", "dia", "yang", "dan", "atau",
    "apa", "itu", "ini", "sih", "dong", "lah",
    "ya", "kok", "deh", "aja", "nih", "nya",
    "banget", "bgt"
}

REPLACE_MAP = {
    "gue": "aku",
    "gw": "aku",
    "gua": "aku",
    "lu": "kamu",
    "loe": "kamu",
    "ga": "tidak",
    "gak": "tidak",
    "nggak": "tidak",
    "cape": "capek",
    "pusing": "capek",
    "berat": "capek",
    "capek": "capek",
    "capek": "capek",
    "lelah": "capek",
    "letih": "capek",
    "ngos": "capek",
    "drop": "capek"
}

MATH_WORDS = {
    "tambah": "+",
    "ditambah": "+",
    "kurang": "-",
    "dikurang": "-",
    "kali": "*",
    "dikali": "*",
    "bagi": "/",
    "dibagi": "/"
}

INTENT_HINTS = {
    "mental": "mental",
    "pikiran": "mental",
    "kerja": "kerja",
    "fisik": "fisik"
}

def normalize(text: str) -> str:
    text = text.lower()
    for k, v in REPLACE_MAP.items():
        text = text.replace(k, v)
    return text

def tokenize(text: str) -> set:
    tokens = re.findall(r"\b\w+\b", text)
    return {t for t in tokens if t not in STOPWORDS}
