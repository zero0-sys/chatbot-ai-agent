import random
from app.text_utils import tokenize

class TokenScoringAlgorithm:
    def __init__(self):
        self.last_answer = None

    def score(self, user_tokens, question_tokens):
        return len(user_tokens & question_tokens)

    def choose_answer(self, candidates):
        answers = []
        for ans in candidates:
            answers.extend([a.strip() for a in ans.split("|")])

        filtered = [a for a in answers if a != self.last_answer]
        final = random.choice(filtered or answers)
        self.last_answer = final
        return final
