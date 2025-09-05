"""
Scoring Model Services

This package contains scoring services that implement evaluation logic
for domain objects, maintaining clean architecture separation.

Uses Strategy Pattern and Factory Pattern to eliminate nested if statements
and coupling between different card types.
"""

# Legacy compatibility exports
from .card_scoring_service import (
    BaseCardScoringService,
    ConservativeScoringService,
    AggressiveScoringService,
    ScenarioAwareScoringService,
    TempoScoringService,
    ControlScoringService,
    ComboScoringService,
)

# New OOP-based exports
from .scoring_strategies import (
    BaseScoringStrategy,
    ConservativeScoringStrategy,
    AggressiveScoringStrategy,
    TempoScoringStrategy,
    ControlScoringStrategy,
    ComboScoringStrategy,
)

from .scoring_factory import ScoringService, ScoringFactory
from .card_scorers import BaseCardScorer

__all__ = [
    # Legacy compatibility
    "BaseCardScoringService",
    "ConservativeScoringService",
    "AggressiveScoringService",
    "ScenarioAwareScoringService",
    "TempoScoringService",
    "ControlScoringService",
    "ComboScoringService",
    # New OOP-based services
    "BaseScoringStrategy",
    "ConservativeScoringStrategy",
    "AggressiveScoringStrategy",
    "TempoScoringStrategy",
    "ControlScoringStrategy",
    "ComboScoringStrategy",
    # Core components
    "ScoringService",
    "ScoringFactory",
    "BaseCardScorer",
]
