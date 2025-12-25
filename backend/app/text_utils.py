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
    "berat": "capek"
}

def normalize(text: str) -> str:
    text = text.lower()
    for k, v in REPLACE_MAP.items():
        text = text.replace(k, v)
    return text

def tokenize(text: str) -> set:
    tokens = re.findall(r"\b\w+\b", text)
    return {t for t in tokens if t not in STOPWORDS}
