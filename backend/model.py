import pandas as pd
import re
import random

STOPWORDS = {
    "aku", "kamu", "dia", "yang", "dan", "atau",
    "apa", "itu", "ini", "sih", "dong", "lah",
    "ya", "kok", "deh", "aja", "nih", "nya"
}

class SimpleChatModel:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df["question"] = self.df["question"].str.lower()
        self.last_answer = None  # ⬅️ penting

    def tokenize(self, text: str):
        tokens = re.findall(r"\b\w+\b", text.lower())
        return {t for t in tokens if t not in STOPWORDS}

    def predict(self, text: str):
        user_tokens = self.tokenize(text)

        best_score = 0
        candidate_answers = []

        for _, row in self.df.iterrows():
            q_tokens = self.tokenize(row["question"])
            score = len(user_tokens & q_tokens)

            if score > best_score:
                best_score = score
                candidate_answers = [row["answer"]]
            elif score == best_score and score > 0:
                candidate_answers.append(row["answer"])

        # ⛔ threshold minimum (WAJIB)
        if best_score < 2:
            return "Aku belum paham maksud kamu. Coba jelasin dengan kata lain."

        # 🎲 variasi jawaban
        answers = []
        for ans in candidate_answers:
            answers.extend([a.strip() for a in ans.split("|")])

        # ❌ cegah jawaban sama berturut-turut
        filtered = [a for a in answers if a != self.last_answer]
        final_answer = random.choice(filtered or answers)

        self.last_answer = final_answer
        return final_answer
