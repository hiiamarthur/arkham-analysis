"""
Shared domain models for Arkham Horror LCG

This package contains domain-specific enums, constants, and types that are
shared between the FastAPI application and the scoring model.

These are pure domain definitions with no dependencies on FastAPI, SQLAlchemy,
or the scoring model implementation.
"""

__version__ = "0.1.0"
__author__ = "Arthur Lau"

from .scenarios import *
from .campaigns import *
from .difficulty import *
from .game_types import *
from .card import *

__all__ = [
    # Difficulty
    "Difficulty",
    # Campaigns
    "CampaignType",
    # Scenarios
    "ScenarioType",
    "SCENARIO_MODIFICATIONS",
    "get_scenario_modifications",
    # Game Types
    "CardType",
    "Faction",
    # "EncounterSet",
    "CycleType",
    # Card
    "ActivationType",
    "CardCostFactor",
    "CardEffect",
    "CardType",
]
