from abc import ABC, abstractmethod
from typing import Any, Dict, List
import sys
import os

# Add the backend directory to Python path to import shared domain types
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Import shared domain types
from domain import (
    Difficulty,
    CampaignType as CAMPAIGNTYPE,
    ScenarioType,
    get_scenario_modifications,
)

from domain.Token.chaos_bag import ChaosBag
from domain.Token.token import (
    AutoFailToken,
    ChaosToken,
    ElderSignToken,
    MinusEightToken,
    MinusFiveToken,
    MinusFourToken,
    MinusOneToken,
    MinusTwoToken,
    MinusThreeToken,
    PlusOneToken,
    SkullToken,
    ZeroToken,
    CultistToken,
    TabletToken,
    ElderThingToken,
)
from .scenario import Scenario
from .components.context_calculator import ContextCalculator

__all__ = ["Scenario", "ContextCalculator"]


# Re-export for backwards compatibility
# def get_scenario_modifications_compat(
#     scenario: ScenarioType, difficulty: Difficulty
# ) -> Dict[str, Dict[str, str]]:
#     """Backwards compatibility wrapper for get_scenario_modifications"""
#     return get_scenario_modifications(scenario, difficulty)


# class Campaign(ABC):
#     def __init__(self, campaign_type: CAMPAIGNTYPE, difficulty: Difficulty):
#         self.campaign_type = campaign_type
#         self.difficulty = difficulty
#         self.chaos_bag = ChaosBag(self.get_init_tokens(difficulty))

#     @abstractmethod
#     def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
#         """Create the chaos bag tokens for this campaign at the given difficulty."""
#         pass


# class Scenario(ABC):
#     def __init__(
#         self,
#         campaign: Campaign,
#         scenario: ScenarioType,
#         difficulty: Difficulty,
#     ):
#         self.campaign = campaign
#         self.scenario = scenario
#         self.difficulty = difficulty
#         self.chaos_bag = campaign.chaos_bag
#         self.scenario_modifications = get_scenario_modifications(scenario, difficulty)

#         # Initialize context values
#         self._doom_threshold = self._calculate_doom_threshold()
#         self._starting_clues = self._calculate_starting_clues()
#         self._agenda_advancement_rate = self._get_agenda_advancement_rate()

#         self._apply_scenario_modifications()

#     def _apply_scenario_modifications(self):
#         """Apply scenario-specific token modifications to chaos bag"""
#         modifications = self._get_scenario_modifications()
#         if modifications:
#             self._modify_special_tokens(modifications)

#     def _get_scenario_modifications(self):
#         """Override in subclasses or use mapping"""
#         return get_scenario_modifications(self.scenario, self.difficulty)

#     def _modify_special_tokens(self, modifications):
#         """Modify special tokens with scenario-specific effects"""
#         from Token.token import (
#             SkullToken,
#             CultistToken,
#             TabletToken,
#             ElderThingToken,
#         )

#         for i, token in enumerate(self.chaos_bag.tokens):
#             if isinstance(token, SkullToken) and "skull" in modifications:
#                 skull_data = modifications["skull"]
#                 self.chaos_bag.tokens[i] = SkullToken(
#                     skull_data.get("effect", ""), skull_data.get("value", token.value)
#                 )
#             elif isinstance(token, CultistToken) and "cultist" in modifications:
#                 cultist_data = modifications["cultist"]
#                 self.chaos_bag.tokens[i] = CultistToken(
#                     cultist_data.get("effect", ""),
#                     cultist_data.get("value", token.value),
#                 )
#             elif isinstance(token, TabletToken) and "tablet" in modifications:
#                 tablet_data = modifications["tablet"]
#                 self.chaos_bag.tokens[i] = TabletToken(
#                     tablet_data.get("effect", ""), tablet_data.get("value", token.value)
#                 )
#             elif isinstance(token, ElderThingToken) and "elder_thing" in modifications:
#                 elder_data = modifications["elder_thing"]
#                 self.chaos_bag.tokens[i] = ElderThingToken(
#                     elder_data.get("effect", ""), elder_data.get("value", token.value)
#                 )

#     # Context Calculation Methods
#     def _calculate_doom_threshold(self) -> int:
#         """Calculate doom threshold for this scenario"""
#         # Base doom threshold varies by scenario
#         scenario_doom_map = {
#             ScenarioType.THE_GATHERING: 7,
#             ScenarioType.THE_MIDNIGHT_MASKS: 9,
#             ScenarioType.THE_DEVOURER_BELOW: 10,
#             # Add more scenarios as needed
#         }
#         base_doom = scenario_doom_map.get(self.scenario, 8)  # Default 8

#         # Difficulty adjustments
#         difficulty_modifiers = {
#             Difficulty.EASY: +2,
#             Difficulty.STANDARD: 0,
#             Difficulty.HARD: -1,
#             Difficulty.EXPERT: -2,
#         }

#         return max(5, base_doom + difficulty_modifiers.get(self.difficulty, 0))

#     def _calculate_starting_clues(self) -> int:
#         """Calculate starting clues based on scenario and player count"""
#         # This would typically be based on player count, but showing the pattern
#         scenario_clues_map = {
#             ScenarioType.THE_GATHERING: 4,
#             ScenarioType.THE_MIDNIGHT_MASKS: 6,
#             ScenarioType.THE_DEVOURER_BELOW: 5,
#         }
#         return scenario_clues_map.get(self.scenario, 4)

#     def _get_agenda_advancement_rate(self) -> float:
#         """Get the rate at which agenda advances (doom per round)"""
#         # Most scenarios advance 1 doom per round, some are faster
#         fast_scenarios = {
#             ScenarioType.THE_DEVOURER_BELOW,  # Accelerated doom
#             ScenarioType.THE_MIDNIGHT_MASKS,  # Time pressure
#         }

#         if self.scenario in fast_scenarios:
#             return (
#                 1.5 if self.difficulty in [Difficulty.HARD, Difficulty.EXPERT] else 1.2
#             )
#         return 1.0

#     # Context Assessment Methods
#     def calculate_time_pressure(self) -> float:
#         """Calculate time pressure context (0.0 to 1.0)"""
#         base_pressure = 0.5  # Neutral pressure

#         # Adjust based on doom threshold vs agenda rate
#         doom_ratio = self._doom_threshold / (
#             self._agenda_advancement_rate * 8
#         )  # 8 rounds typical game

#         if doom_ratio < 0.8:
#             base_pressure += 0.3  # High pressure
#         elif doom_ratio > 1.2:
#             base_pressure -= 0.2  # Low pressure

#         return max(0.0, min(1.0, base_pressure))

#     def calculate_resource_scarcity(self) -> float:
#         """Calculate resource scarcity context (0.0 to 1.0)"""
#         base_scarcity = 0.4  # Slightly resource constrained

#         # Scenarios with fewer clues are more resource-constrained
#         if self._starting_clues < 4:
#             base_scarcity += 0.2
#         elif self._starting_clues > 6:
#             base_scarcity -= 0.2

#         # Harder difficulties have more resource constraints
#         difficulty_modifiers = {
#             Difficulty.EASY: -0.2,
#             Difficulty.STANDARD: 0.0,
#             Difficulty.HARD: +0.1,
#             Difficulty.EXPERT: +0.2,
#         }

#         base_scarcity += difficulty_modifiers.get(self.difficulty, 0)
#         return max(0.0, min(1.0, base_scarcity))

#     def calculate_chaos_bag_hostility(self) -> float:
#         """Calculate how hostile the chaos bag is (0.0 to 1.0)"""
#         total_tokens = len(self.chaos_bag.tokens)
#         negative_value = 0

#         for token in self.chaos_bag.tokens:
#             if hasattr(token, "value") and isinstance(token.value, (int, float)):
#                 if token.value < 0:
#                     negative_value += abs(token.value)

#         # Normalize based on typical chaos bag composition
#         hostility = min(1.0, negative_value / (total_tokens * 2))  # Rough normalization
#         return hostility

#     def get_scenario_context(self) -> Dict[str, float]:
#         """Get comprehensive scenario context for card evaluation"""
#         return {
#             "time_pressure": self.calculate_time_pressure(),
#             "resource_scarcity": self.calculate_resource_scarcity(),
#             "chaos_hostility": self.calculate_chaos_bag_hostility(),
#             "doom_threshold": float(self._doom_threshold),
#             "starting_clues": float(self._starting_clues),
#             "agenda_rate": self._agenda_advancement_rate,
#         }

#     def get_initial_context_values(self) -> Dict[str, Any]:
#         """Get initial context values for scenario setup"""
#         return {
#             "doom_threshold": self._doom_threshold,
#             "starting_clues": self._starting_clues,
#             "agenda_advancement_rate": self._agenda_advancement_rate,
#             "difficulty": self.difficulty,
#             "scenario_type": self.scenario,
#             "campaign_type": self.campaign.campaign_type,
#         }


# class NightOfTheZealot(Campaign):

#     def __init__(self, difficulty: Difficulty):
#         super().__init__(CAMPAIGNTYPE.NIGHT_OF_THE_ZEALOT, difficulty)

#     def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
#         base_tokens = [
#             ElderSignToken(),
#             AutoFailToken(),
#         ]

#         token_configs = {
#             Difficulty.EASY: {
#                 PlusOneToken: 2,
#                 ZeroToken: 3,
#                 MinusOneToken: 3,
#                 MinusTwoToken: 2,
#             },
#             Difficulty.STANDARD: {
#                 PlusOneToken: 1,
#                 ZeroToken: 2,
#                 MinusOneToken: 3,
#                 MinusTwoToken: 2,
#                 MinusThreeToken: 1,
#                 MinusFourToken: 1,
#             },
#             Difficulty.HARD: {
#                 ZeroToken: 3,
#                 MinusOneToken: 2,
#                 MinusTwoToken: 2,
#                 MinusThreeToken: 2,
#                 MinusFourToken: 1,
#             },
#             Difficulty.EXPERT: {
#                 ZeroToken: 1,
#                 MinusOneToken: 2,
#                 MinusTwoToken: 2,
#                 MinusThreeToken: 3,
#                 MinusFourToken: 4,
#                 MinusFiveToken: 1,
#                 MinusEightToken: 1,
#             },
#         }

#         config = token_configs.get(difficulty, {})
#         for token_type, count in config.items():
#             if isinstance(token_type, tuple):
#                 token_class, *args = token_type
#                 base_tokens.extend([token_class(*args) for _ in range(count)])
#             else:
#                 base_tokens.extend([token_type() for _ in range(count)])

#         return base_tokens


# class TheDunwichLegacy(Campaign):
#     def __init__(self, difficulty: Difficulty):
#         super().__init__(CAMPAIGNTYPE.THE_DUNWICH_LEGACY, difficulty)

#     def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
#         base_tokens = [
#             ElderSignToken(),
#             AutoFailToken(),
#         ]

#         token_configs = {
#             Difficulty.EASY: {
#                 PlusOneToken: 1,
#                 ZeroToken: 2,
#                 MinusOneToken: 2,
#                 MinusTwoToken: 2,
#                 (SkullToken, "", -1): 1,
#                 (SkullToken, "", -2): 1,
#             },
#             Difficulty.STANDARD: {
#                 ZeroToken: 1,
#                 MinusOneToken: 2,
#                 MinusTwoToken: 2,
#                 (SkullToken, "", -2): 1,
#                 (SkullToken, "", -3): 1,
#             },
#             Difficulty.HARD: {
#                 ZeroToken: 1,
#                 MinusOneToken: 1,
#                 MinusTwoToken: 1,
#                 (SkullToken, "", -3): 1,
#                 (SkullToken, "", -4): 1,
#             },
#             Difficulty.EXPERT: {
#                 MinusOneToken: 1,
#                 (SkullToken, "", -4): 1,
#                 (SkullToken, "", -5): 1,
#             },
#         }

#         config = token_configs.get(difficulty, {})
#         for token_type, count in config.items():
#             if isinstance(token_type, tuple):
#                 token_class, *args = token_type
#                 base_tokens.extend([token_class(*args) for _ in range(count)])
#             else:
#                 base_tokens.extend([token_type() for _ in range(count)])

#         return base_tokens


# # Scenario factory function
# def create_scenario(
#     campaign: Campaign, scenario_type: ScenarioType, difficulty: Difficulty
# ) -> Scenario:
#     """Factory function to create scenarios with proper chaos bag modifications"""

#     class DynamicScenario(Scenario):
#         pass

#     return DynamicScenario(campaign, scenario_type, difficulty)


# # Convenience functions for specific campaigns
# def create_night_of_zealot_scenario(
#     difficulty: Difficulty, scenario_type: ScenarioType
# ) -> Scenario:
#     """Create Night of the Zealot scenario"""
#     campaign = NightOfTheZealot(difficulty)
#     return create_scenario(campaign, scenario_type, difficulty)


# def create_dunwich_scenario(
#     difficulty: Difficulty, scenario_type: ScenarioType
# ) -> Scenario:
#     """Create Dunwich Legacy scenario"""
#     campaign = TheDunwichLegacy(difficulty)
#     return create_scenario(campaign, scenario_type, difficulty)
