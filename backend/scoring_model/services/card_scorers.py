"""
Individual card scorer implementations using Strategy Pattern
Each card type has its own scorer to eliminate nested if statements and coupling
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from domain.card.base_card import BaseCard
from domain.card.player_card import PlayerCard
from domain.card.asset_card import AssetCard
from domain.card.event_card import EventCard
from domain.card.skill_card import SkillCard
from domain.card.investigator_card import InvestigatorCard
from domain.card.encounter_card import EncounterCard
from domain.card.scenario_card import ScenarioCard
from domain.card import CardCostFactor, CardType


class BaseCardScorer(ABC):
    """Abstract base class for all card scorers"""

    def __init__(self, weights: Dict[str, float]):
        self.weights = weights

    @abstractmethod
    def calculate_cost(self, card: BaseCard) -> float:
        """Calculate the cost/negative value of a card"""
        pass

    @abstractmethod
    def calculate_gain(self, card: BaseCard) -> float:
        """Calculate the gain/positive value of a card"""
        pass

    def calculate_net_value(self, card: BaseCard) -> float:
        """Calculate net value (gain - cost)"""
        return self.calculate_gain(card) - self.calculate_cost(card)


class PlayerCardScorer(BaseCardScorer):
    """Scorer for all player cards (Asset, Event, Skill, Investigator)"""

    def calculate_cost(self, card: PlayerCard) -> float:
        """Calculate cost for player cards"""
        cost = 0.0
        # Action cost
        action_cost = (
            card.play_action_cost
            * card.cost_factors[CardCostFactor.ACTION]
            * self.weights["action"]
        )
        if hasattr(card, "activation_type"):
            if card.activation_type.value == "Fast":
                action_cost *= self.weights["fast_action"]
            elif card.activation_type.value == "Reaction":
                action_cost *= self.weights["reaction"]

        cost += action_cost

        # Resource cost
        cost += card.cost * card.cost_factors[CardCostFactor.RESOURCE]

        # XP cost
        # cost += card.level * self.weights["xp"]

        # Opportunity cost from skill icons
        skill_icons = (
            card.skill_agility
            + card.skill_combat
            + card.skill_intellect
            + card.skill_willpower
            + card.skill_wild
        )
        cost += skill_icons * self.weights["icon"]

        # Wild icons are more valuable
        cost += card.skill_wild * (self.weights["wild_icon"] - self.weights["icon"])

        # Card property modifiers
        if card.is_unique:
            cost += self.weights["unique"]
        if card.is_permanent:
            cost += self.weights["permanent"]
        if hasattr(card, "is_exceptional") and getattr(card, "is_exceptional", False):
            cost += self.weights["exceptional"]

        return cost

    def calculate_gain(self, card: PlayerCard) -> float:
        """Calculate gain for player cards"""
        gain = 0.0

        # Skill icon value
        skill_icons = (
            card.skill_agility
            + card.skill_combat
            + card.skill_intellect
            + card.skill_willpower
            + card.skill_wild
        )
        gain += skill_icons * self.weights["icon"]

        # Wild icons are more valuable
        gain += card.skill_wild * (self.weights["wild_icon"] - self.weights["icon"])

        return gain


class AssetCardScorer(PlayerCardScorer):
    """Specialized scorer for Asset cards"""

    def calculate_gain(self, card: AssetCard) -> float:
        """Calculate gain for asset cards with health/sanity bonuses"""
        gain = super().calculate_gain(card)

        # Health/Sanity for assets
        if hasattr(card, "health") and card.health > 0:
            gain += card.health * self.weights["health"]
        if hasattr(card, "sanity") and card.sanity > 0:
            gain += card.sanity * self.weights["sanity"]

        # Assets provide ongoing value
        gain *= 1.0  # Base multiplier for assets

        return gain


class EventCardScorer(PlayerCardScorer):
    """Specialized scorer for Event cards"""

    def calculate_gain(self, card: EventCard) -> float:
        """Calculate gain for event cards"""
        gain = super().calculate_gain(card)

        # Events are one-time use but powerful
        gain *= 1.1

        return gain


class SkillCardScorer(PlayerCardScorer):
    """Specialized scorer for Skill cards"""

    def calculate_gain(self, card: SkillCard) -> float:
        """Calculate gain for skill cards"""
        gain = super().calculate_gain(card)

        # Skills provide immediate value
        gain *= 1.2

        return gain


class InvestigatorCardScorer(PlayerCardScorer):
    """Specialized scorer for Investigator cards"""

    def calculate_gain(self, card: PlayerCard) -> float:
        """Calculate gain for investigator cards"""
        gain = super().calculate_gain(card)

        # Investigators have special abilities and stats
        # This would need more specific implementation based on investigator abilities
        gain *= 1.5  # Investigators are very valuable

        return gain


class EncounterCardScorer(BaseCardScorer):
    """Scorer for encounter cards"""

    def calculate_cost(self, card: EncounterCard) -> float:
        """Calculate cost for encounter cards (threat level)"""
        cost = 0.0

        # Base threat based on card type
        if card.card_type == CardType.ENEMY:
            cost += 2.0  # Enemies are generally threatening
        elif card.card_type == CardType.TREACHERY:
            cost += 1.5  # Treacheries can be nasty
        elif card.card_type == CardType.LOCATION:
            cost += 1.0  # Locations have mixed effects

        return cost

    def calculate_gain(self, card: EncounterCard) -> float:
        """Calculate gain for encounter cards (positive effects)"""
        gain = 0.0

        # Some encounter cards can have positive effects
        # This would need to be implemented based on specific card text analysis
        # For now, most encounter cards have negative or neutral value

        return gain


class ScenarioCardScorer(BaseCardScorer):
    """Scorer for scenario cards (Act, Agenda, etc.)"""

    def calculate_cost(self, card: ScenarioCard) -> float:
        """Calculate cost for scenario cards"""
        # Scenario cards typically don't have player costs
        return 0.0

    def calculate_gain(self, card: ScenarioCard) -> float:
        """Calculate gain for scenario cards"""
        # Scenario cards provide scenario structure, not player value
        return 0.0


class UnknownCardScorer(BaseCardScorer):
    """Fallback scorer for unknown card types"""

    def calculate_cost(self, card: BaseCard) -> float:
        """Default cost for unknown cards"""
        return 0.0

    def calculate_gain(self, card: BaseCard) -> float:
        """Default gain for unknown cards"""
        return 0.0
