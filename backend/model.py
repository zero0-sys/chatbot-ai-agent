import pandas as pd
import re
import random

# kata umum yang dibuang
STOPWORDS = {
    "aku", "kamu", "dia", "yang", "dan", "atau",
    "apa", "itu", "ini", "sih", "dong", "lah",
    "ya", "kok", "deh", "aja", "nih", "nya",
    "banget", "bgt"
}

# normalisasi bahasa sehari-hari
REPLACE_MAP = {
    "gue": "aku",
    "gw": "aku",
    "gua": "aku",
    "lu": "kamu",
    "loe": "kamu",
    "ga": "tidak",
    "gak": "tidak",
    "nggak": "tidak",
    "enggak": "tidak",
    "cape": "capek",
    "capek banget": "capek",
    "pusing": "capek",
    "berat": "capek"
}

class SimpleChatModel:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df["question"] = self.df["question"].str.lower()
        self.last_answer = None

    def normalize(self, text: str):
        text = text.lower()
        for k, v in REPLACE_MAP.items():
            text = text.replace(k, v)
        return text

    def tokenize(self, text: str):
        tokens = re.findall(r"\b\w+\b", text)
        return {t for t in tokens if t not in STOPWORDS}

    def predict(self, text: str):
        text = self.normalize(text)
        user_tokens = self.tokenize(text)

        best_score = 0
        candidates = []

        for _, row in self.df.iterrows():
            q_tokens = self.tokenize(row["question"])
            score = len(user_tokens & q_tokens)

            if score > best_score:
                best_score = score
                candidates = [row["answer"]]
            elif score == best_score and score > 0:
                candidates.append(row["answer"])

        # threshold minimum biar ga ngawur
        if best_score < 1:
            return "Aku belum paham maksud kamu. Coba jelasin dengan kata lain ya."

        # variasi jawaban + cegah ngulang
        answers = []
        for ans in candidates:
            answers.extend([a.strip() for a in ans.split("|")])

        filtered = [a for a in answers if a != self.last_answer]
        final = random.choice(filtered or answers)

        self.last_answer = final
        return final
