"""
Scoring Factory using Factory Pattern to create appropriate scorers
Eliminates coupling and nested if statements by delegating to specific scorers
"""

from typing import Dict, Type
from domain.card.base_card import BaseCard
from domain.card.player_card import PlayerCard
from domain.card.asset_card import AssetCard
from domain.card.event_card import EventCard
from domain.card.skill_card import SkillCard
from domain.card.investigator_card import InvestigatorCard
from domain.card.encounter_card import EncounterCard
from domain.card.scenario_card import ScenarioCard
from domain.card import CardType

from .card_scorers import (
    BaseCardScorer,
    PlayerCardScorer,
    AssetCardScorer,
    EventCardScorer,
    SkillCardScorer,
    InvestigatorCardScorer,
    EncounterCardScorer,
    ScenarioCardScorer,
    UnknownCardScorer,
)


class ScoringFactory:
    """Factory for creating appropriate card scorers based on card type"""

    def __init__(self, weights: Dict[str, float]):
        self.weights = weights
        self._scorer_cache: Dict[Type, BaseCardScorer] = {}

    def get_scorer(self, card: BaseCard) -> BaseCardScorer:
        """Get the appropriate scorer for a card type"""
        card_type = type(card)

        # Use cache to avoid creating new instances
        if card_type not in self._scorer_cache:
            self._scorer_cache[card_type] = self._create_scorer(card)

        return self._scorer_cache[card_type]

    def _create_scorer(self, card: BaseCard) -> BaseCardScorer:
        """Create a new scorer instance based on card type"""
        # Use isinstance checks in order of specificity (most specific first)
        if isinstance(card, AssetCard):
            return AssetCardScorer(self.weights)
        elif isinstance(card, EventCard):
            return EventCardScorer(self.weights)
        elif isinstance(card, SkillCard):
            return SkillCardScorer(self.weights)
        elif isinstance(card, InvestigatorCard):
            return InvestigatorCardScorer(self.weights)
        elif isinstance(card, PlayerCard):
            return PlayerCardScorer(self.weights)
        elif isinstance(card, EncounterCard):
            return EncounterCardScorer(self.weights)
        elif isinstance(card, ScenarioCard):
            return ScenarioCardScorer(self.weights)
        else:
            return UnknownCardScorer(self.weights)

    def calculate_cost(self, card: BaseCard) -> float:
        """Calculate cost using appropriate scorer"""
        scorer = self.get_scorer(card)
        return scorer.calculate_cost(card)

    def calculate_gain(self, card: BaseCard) -> float:
        """Calculate gain using appropriate scorer"""
        scorer = self.get_scorer(card)
        return scorer.calculate_gain(card)

    def calculate_net_value(self, card: BaseCard) -> float:
        """Calculate net value using appropriate scorer"""
        scorer = self.get_scorer(card)
        return scorer.calculate_net_value(card)


class ScoringService:
    """Main scoring service that uses the factory pattern"""

    def __init__(self, weights: Dict[str, float] = {}):
        self.weights = weights or self._get_default_weights()
        self.factory = ScoringFactory(self.weights)

    def _get_default_weights(self) -> Dict[str, float]:
        """Default scoring weights - should be configurable"""
        return {
            # Action costs
            "action": 1.0,
            "fast_action": 0.5,
            "reaction": 0.3,
            # Resource costs
            "resource": 1.0,
            "xp": 2.0,
            # Skill icons
            "icon": 0.5,
            "wild_icon": 0.7,
            # Card properties
            "unique": 0.2,
            "permanent": 0.3,
            "exceptional": 0.5,
            # Health/Sanity
            "health": 0.8,
            "sanity": 0.8,
            # Encounter card specific
            "enemy_fight": 1.0,
            "enemy_evade": 1.0,
            "enemy_health": 1.0,
            "location_shroud": 1.0,
            "location_clues": 1.0,
        }

    def calculate_cost(self, card: BaseCard) -> float:
        """Calculate cost for any card type"""
        return self.factory.calculate_cost(card)

    def calculate_gain(self, card: BaseCard) -> float:
        """Calculate gain for any card type"""
        return self.factory.calculate_gain(card)

    def calculate_net_value(self, card: BaseCard) -> float:
        """Calculate net value for any card type"""
        return self.factory.calculate_net_value(card)

    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """Update scoring weights and clear cache"""
        self.weights.update(new_weights)
        self.factory = ScoringFactory(self.weights)
