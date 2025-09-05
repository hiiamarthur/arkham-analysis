"""
Card Scoring Service - Legacy compatibility layer

This module provides backward compatibility for the old scoring service interface.
New code should use the OOP-based scoring services from scoring_strategies.py
"""

from typing import Dict, Any
from .scoring_strategies import (
    BaseScoringStrategy,
    ConservativeScoringStrategy,
    AggressiveScoringStrategy,
    TempoScoringStrategy,
    ControlScoringStrategy,
    ComboScoringStrategy,
)

# Legacy compatibility aliases
BaseCardScoringService = BaseScoringStrategy
ConservativeScoringService = ConservativeScoringStrategy
AggressiveScoringService = AggressiveScoringStrategy

# New strategy-based services
TempoScoringService = TempoScoringStrategy
ControlScoringService = ControlScoringStrategy
ComboScoringService = ComboScoringStrategy


class ScenarioAwareScoringService(BaseScoringStrategy):
    """Scoring service that considers scenario context"""

    def __init__(
        self,
        weights: Dict[str, float] | None = None,
        scenario_context: Dict[str, Any] | None = None,
    ):
        super().__init__(weights or {})
        self.scenario_context = scenario_context or {}

    def calculate_gain(self, card) -> float:
        """Calculate gain considering scenario context"""
        base_gain = super().calculate_gain(card)

        # Adjust based on scenario context
        if self.scenario_context:
            base_gain = self._adjust_for_scenario(card, base_gain)

        return base_gain

    def _adjust_for_scenario(self, card, base_gain: float) -> float:
        """Adjust scoring based on scenario context"""
        # This would implement scenario-specific adjustments
        # For example, if scenario has many enemies, combat icons are more valuable
        # If scenario has many clues, intellect icons are more valuable

        # Placeholder implementation
        return base_gain
