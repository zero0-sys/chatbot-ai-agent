from pydoc import text
from typing import Self
import pandas as pd
from app.text_utils import normalize, tokenize
from app.algorithm import TokenScoringAlgorithm

class ChatModel:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self.df["question"] = self.df["question"].str.lower()
        self.algorithm = TokenScoringAlgorithm()

    def predict(self, text: str):
        text = normalize(text)
        user_tokens = tokenize(text)

        best_score = 0
        candidates = []

        for _, row in self.df.iterrows():
            q_tokens = tokenize(row["question"])
            score = len(user_tokens & q_tokens)

            if score > best_score:
                best_score = score
                candidates = [row["answer"]]
            elif score == best_score and score > 0:
                candidates.append(row["answer"])

        if best_score < 1:
            return (
                "Aku belum paham maksud kamu. Bisa jelasin dengan kata lain?",
                0
            )

        answer = self.algorithm.choose_answer(candidates)
        return answer, best_score
