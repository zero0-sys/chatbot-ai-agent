import pandas as pd
from app.text_utils import normalize, tokenize
from app.algorithm import TokenScoringAlgorithm


class ChatModel:
    def __init__(self, csv_path: str):
        # load training data
        self.df = pd.read_csv(csv_path)

        # pastikan kolom ada
        if "question" not in self.df.columns or "answer" not in self.df.columns:
            raise ValueError("CSV harus punya kolom: question, answer")

        # normalisasi pertanyaan di awal
        self.df["question"] = self.df["question"].astype(str).str.lower()

        # algoritma scoring
        self.algorithm = TokenScoringAlgorithm()

    def predict(self, text: str):
        """
        return:
          - reply (str)
          - confidence (int) -> dipakai buat learning decision
        """

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
        # PILIH JAWABAN (ANTI NGULANG)
        # =========================
        final_answer = self.algorithm.choose_answer(candidates)

        return final_answer, best_score
