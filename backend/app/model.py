import pandas as pd
import random
from app.text_utils import normalize, tokenize
from app.algorithm import TokenScoringAlgorithm


class ChatModel:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path, on_bad_lines="skip", engine="python")
        self.last_answer = None  # 🔥 SIMPAN JAWABAN TERAKHIR

        if "question" not in self.df.columns or "answer" not in self.df.columns:
            raise ValueError("CSV harus punya kolom: question, answer")

        self.df["question"] = self.df["question"].astype(str).str.lower()

        self.algorithm = TokenScoringAlgorithm()

    def predict(self, text: str):
        # =========================
        # NORMALISASI USER INPUT
        # =========================
        text_norm = normalize(text)
        user_tokens = tokenize(text_norm)

        best_score = 0
        candidates = []

        # =========================
        # SCORING TOKEN MATCH
        # =========================
        for _, row in self.df.iterrows():
            q_tokens = tokenize(row["question"])
            score = len(user_tokens & q_tokens)

            if score > best_score:
                best_score = score
                candidates = [row["answer"]]
            elif score == best_score and score > 0:
                candidates.append(row["answer"])

        # =========================
        # JIKA TIDAK PAHAM
        # =========================
        if best_score < 1:
            return (
                "Aku belum paham maksud kamu. Bisa jelasin dengan kata lain?",
                0
            )

        # =========================
        # 🔥 EXPAND JAWABAN (|)
        # =========================
        expanded_answers = []
        for ans in candidates:
            parts = [a.strip() for a in ans.split("|") if a.strip()]
            expanded_answers.extend(parts)

        # =========================
        # 🔥 ANTI NGULANG JAWABAN
        # =========================
        if self.last_answer in expanded_answers and len(expanded_answers) > 1:
            expanded_answers.remove(self.last_answer)

        # =========================
        # PILIH RANDOM
        # =========================
        final_answer = random.choice(expanded_answers)

        # SIMPAN JAWABAN TERAKHIR
        self.last_answer = final_answer

        return final_answer, best_score
