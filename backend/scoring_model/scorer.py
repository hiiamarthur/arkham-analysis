from .models import CardData, ScoreResult
from .evaluators.base_evalutor import BaseEvaluator


class CardScorer:
    def __init__(self, evaluator=None):
        # Allow custom evaluators (e.g., basic, weighted, ai-based in future)
        self.evaluator = evaluator or BaseEvaluator()

    def calculate_card_value(self, card_data: CardData) -> ScoreResult:
        """
        Main method to calculate the strength value of a card.
        """
        # score = self.evaluator.(card_data)
        return ScoreResult(card_id=card_data.card_id, strength_score=0)
