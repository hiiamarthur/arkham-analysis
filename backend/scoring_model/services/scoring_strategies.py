"""
Scoring Strategy implementations using Strategy Pattern
Different scoring strategies with different weight configurations
"""

from typing import Dict
from .scoring_factory import ScoringService


class BaseScoringStrategy(ScoringService):
    """Base scoring strategy with balanced weights"""

    def _get_default_weights(self) -> Dict[str, float]:
        """Balanced scoring weights"""
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


class ConservativeScoringStrategy(ScoringService):
    """Conservative scoring that values safety and efficiency"""

    def _get_default_weights(self) -> Dict[str, float]:
        """Conservative scoring weights"""
        weights = super()._get_default_weights()
        weights.update(
            {
                "action": 1.2,  # Actions are more expensive
                "resource": 1.1,  # Resources are more valuable
                "health": 1.0,  # Health is very important
                "sanity": 1.0,  # Sanity is very important
                "unique": 0.3,  # Unique cards are more valuable
                "permanent": 0.4,  # Permanent cards are more valuable
            }
        )
        return weights


class AggressiveScoringStrategy(ScoringService):
    """Aggressive scoring that values power and tempo"""

    def _get_default_weights(self) -> Dict[str, float]:
        """Aggressive scoring weights"""
        weights = super()._get_default_weights()
        weights.update(
            {
                "action": 0.8,  # Actions are cheaper (tempo focused)
                "resource": 0.9,  # Resources are less valuable
                "icon": 0.6,  # Skill icons are more valuable
                "wild_icon": 0.8,  # Wild icons are very valuable
                "fast_action": 0.3,  # Fast actions are much more valuable
                "exceptional": 0.3,  # Exceptional cards are less penalized
            }
        )
        return weights


class TempoScoringStrategy(ScoringService):
    """Tempo-focused scoring that values speed and efficiency"""

    def _get_default_weights(self) -> Dict[str, float]:
        """Tempo scoring weights"""
        weights = super()._get_default_weights()
        weights.update(
            {
                "action": 0.7,  # Actions are very cheap
                "fast_action": 0.2,  # Fast actions are extremely valuable
                "reaction": 0.1,  # Reactions are extremely valuable
                "resource": 0.8,  # Resources are less important
                "icon": 0.7,  # Skill icons are very valuable
                "wild_icon": 0.9,  # Wild icons are extremely valuable
            }
        )
        return weights


class ControlScoringStrategy(ScoringService):
    """Control-focused scoring that values long-term value and efficiency"""

    def _get_default_weights(self) -> Dict[str, float]:
        """Control scoring weights"""
        weights = super()._get_default_weights()
        weights.update(
            {
                "action": 1.3,  # Actions are expensive (value efficiency)
                "resource": 1.2,  # Resources are very valuable
                "health": 1.2,  # Health is extremely important
                "sanity": 1.2,  # Sanity is extremely important
                "permanent": 0.5,  # Permanent cards are very valuable
                "unique": 0.4,  # Unique cards are very valuable
                "xp": 2.5,  # XP is very expensive
            }
        )
        return weights


class ComboScoringStrategy(ScoringService):
    """Combo-focused scoring that values synergy and card interactions"""

    def _get_default_weights(self) -> Dict[str, float]:
        """Combo scoring weights"""
        weights = super()._get_default_weights()
        weights.update(
            {
                "icon": 0.8,  # Skill icons are very valuable for combos
                "wild_icon": 1.0,  # Wild icons are extremely valuable
                "unique": 0.1,  # Unique cards are less penalized
                "exceptional": 0.2,  # Exceptional cards are less penalized
                "action": 0.9,  # Actions are slightly cheaper
                "resource": 0.9,  # Resources are slightly less valuable
            }
        )
        return weights
