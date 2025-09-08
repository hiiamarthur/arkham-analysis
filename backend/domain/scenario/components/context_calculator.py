"""
Context Calculator - Calculates scenario context values for card evaluation
Follows SRP by focusing solely on context calculation logic
"""

from typing import Dict, Optional, Any
from domain.Token.chaos_bag import ChaosBag

import sys
import os

backend_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."
)
if backend_path not in sys.path:
    sys.path.append(backend_path)

from domain.scenario.rules.scenario_definitions import get_scenario_rules
from domain import ScenarioType, Difficulty


class ContextCalculator:
    """Calculates various scenario context values for informed card evaluation"""

    def __init__(
        self, scenario_type: ScenarioType, difficulty: Difficulty, player_count: int = 2
    ):
        self.scenario_type = scenario_type
        self.difficulty = difficulty
        self.player_count = player_count

        # Context calculation parameters (can be tuned)
        self.time_pressure_weights = {
            "doom_ratio": 0.4,
            "scenario_speed": 0.3,
            "difficulty": 0.3,
        }

        self.resource_weights = {
            "clue_availability": 0.5,
            "difficulty": 0.3,
            "scenario_complexity": 0.2,
        }

        # Initialize context with player_count for rule application
        self.context = {
            "player_count": player_count,
            "difficulty": difficulty.value,
            "scenario_type": scenario_type.value,
        }

        # Load and apply scenario rules
        self.rules = get_scenario_rules(scenario_type)
        for rule in self.rules:
            self.context = rule.apply(self.context)

    def get_scenario_values(self) -> Dict[str, Any]:
        """Get calculated scenario values from rules"""
        return self.context.copy()

    def calculate_time_pressure(
        self, doom_threshold: int, agenda_rate: float, player_count: int = 2
    ) -> float:
        """
        Calculate time pressure context (0.0 to 1.0)
        Higher values indicate more time pressure
        """
        base_pressure = 0.5  # Neutral starting point

        # Factor 1: Doom threshold vs typical game length
        typical_game_rounds = 8
        doom_ratio = doom_threshold / (agenda_rate * typical_game_rounds)

        if doom_ratio < 0.6:  # Very tight time limit
            doom_pressure = 0.8
        elif doom_ratio < 0.8:  # Tight time limit
            doom_pressure = 0.6
        elif doom_ratio > 1.4:  # Generous time limit
            doom_pressure = 0.2
        else:  # Standard time limit
            doom_pressure = 0.4

        # Factor 2: Scenario-specific speed modifiers
        scenario_speed = self._get_scenario_speed_modifier()

        # Factor 3: Difficulty impact on time pressure
        difficulty_pressure = self._get_difficulty_time_modifier()

        # Weighted combination
        final_pressure = (
            doom_pressure * self.time_pressure_weights["doom_ratio"]
            + scenario_speed * self.time_pressure_weights["scenario_speed"]
            + difficulty_pressure * self.time_pressure_weights["difficulty"]
        )

        return max(0.0, min(1.0, final_pressure))

    def calculate_resource_scarcity(
        self, starting_clues: int, player_count: int = 2
    ) -> float:
        """
        Calculate resource scarcity context (0.0 to 1.0)
        Higher values indicate more resource constraints
        """
        base_scarcity = 0.4  # Slightly resource constrained baseline

        # Factor 1: Clues per player ratio
        clues_per_player = starting_clues / player_count
        if clues_per_player < 2:
            clue_scarcity = 0.8
        elif clues_per_player < 3:
            clue_scarcity = 0.6
        elif clues_per_player > 4:
            clue_scarcity = 0.2
        else:
            clue_scarcity = 0.4

        # Factor 2: Difficulty impact on resources
        difficulty_scarcity = self._get_difficulty_resource_modifier()

        # Factor 3: Scenario complexity (more complex = more resource intensive)
        complexity_scarcity = self._get_scenario_complexity_modifier()

        # Weighted combination
        final_scarcity = (
            clue_scarcity * self.resource_weights["clue_availability"]
            + difficulty_scarcity * self.resource_weights["difficulty"]
            + complexity_scarcity * self.resource_weights["scenario_complexity"]
        )

        return max(0.0, min(1.0, final_scarcity))

    def calculate_chaos_hostility(self, chaos_bag: ChaosBag) -> float:
        """
        Calculate chaos bag hostility (0.0 to 1.0)
        Higher values indicate more hostile chaos bag
        """
        total_tokens = len(chaos_bag.tokens)
        if total_tokens == 0:
            return 0.0

        negative_impact = 0
        auto_fail_count = 0
        special_token_penalty = 0

        for token in chaos_bag.tokens:
            # Handle numeric tokens
            if hasattr(token, "value") and isinstance(token.value, (int, float)):
                if token.value < 0:
                    negative_impact += abs(token.value)

            # Handle special tokens
            token_name = token.__class__.__name__.lower()
            if "autofail" in token_name:
                auto_fail_count += 1
            elif any(
                special in token_name
                for special in ["skull", "cultist", "tablet", "elderthing"]
            ):
                special_token_penalty += 2  # Special tokens add uncertainty

        # Calculate hostility components
        numeric_hostility = min(1.0, negative_impact / (total_tokens * 3))  # Normalize
        auto_fail_hostility = min(0.3, auto_fail_count * 0.15)  # Auto-fail cap
        special_hostility = min(
            0.4, special_token_penalty / total_tokens
        )  # Special token impact

        return min(1.0, numeric_hostility + auto_fail_hostility + special_hostility)

    def calculate_encounter_difficulty(self) -> float:
        """
        Calculate overall encounter difficulty (0.0 to 1.0)
        Based on scenario and difficulty combination
        """
        # Base difficulty from difficulty setting
        difficulty_base = {
            Difficulty.EASY: 0.2,
            Difficulty.STANDARD: 0.4,
            Difficulty.HARD: 0.7,
            Difficulty.EXPERT: 0.9,
        }.get(self.difficulty, 0.4)

        # Scenario-specific difficulty modifiers
        scenario_modifier = self._get_scenario_difficulty_modifier()

        return max(0.0, min(1.0, difficulty_base + scenario_modifier))

    def calculate_full_context(
        self,
        doom_threshold: int,
        starting_clues: int,
        agenda_rate: float,
        chaos_bag: ChaosBag,
        player_count,
    ) -> Dict[str, float]:
        """Calculate comprehensive scenario context"""
        return {
            "time_pressure": self.calculate_time_pressure(
                doom_threshold, agenda_rate, player_count
            ),
            # "resource_scarcity": self.calculate_resource_scarcity(
            #     starting_clues, player_count
            # ),
            "chaos_hostility": self.calculate_chaos_hostility(chaos_bag),
            "encounter_difficulty": self.calculate_encounter_difficulty(),
            "doom_threshold": float(doom_threshold),
            "starting_clues": float(starting_clues),
            "agenda_rate": agenda_rate,
            "player_count": float(player_count),
        }

    def _get_scenario_speed_modifier(self) -> float:
        """Get scenario-specific speed pressure modifier"""
        # Fast-paced scenarios with time pressure
        fast_scenarios = {
            ScenarioType.THE_MIDNIGHT_MASKS,  # Time pressure mechanics
            ScenarioType.THE_DEVOURER_BELOW,  # Accelerated doom
            ScenarioType.THE_ESSEX_COUNTRY_EXPRESS,  # Moving train
        }

        # Slow-paced scenarios with more time
        slow_scenarios = {
            ScenarioType.THE_GATHERING,  # Tutorial scenario
            ScenarioType.THE_MISKATONIC_MUSEUM,  # Investigation focused
        }

        if self.scenario_type in fast_scenarios:
            return 0.7
        elif self.scenario_type in slow_scenarios:
            return 0.2
        else:
            return 0.4  # Standard pace

    def _get_difficulty_time_modifier(self) -> float:
        """Get difficulty-based time pressure modifier"""
        return {
            Difficulty.EASY: 0.2,
            Difficulty.STANDARD: 0.4,
            Difficulty.HARD: 0.6,
            Difficulty.EXPERT: 0.8,
        }.get(self.difficulty, 0.4)

    def _get_difficulty_resource_modifier(self) -> float:
        """Get difficulty-based resource scarcity modifier"""
        return {
            Difficulty.EASY: 0.1,
            Difficulty.STANDARD: 0.3,
            Difficulty.HARD: 0.6,
            Difficulty.EXPERT: 0.8,
        }.get(self.difficulty, 0.3)

    def _get_scenario_complexity_modifier(self) -> float:
        """Get scenario complexity modifier for resource requirements"""
        # Complex scenarios require more resources/actions
        complex_scenarios = {
            ScenarioType.THE_PALLID_MASK,  # Multiple locations, complex mechanics
            ScenarioType.DIM_CARCOSA,  # Final scenario complexity
            ScenarioType.SHATTERED_AEONS,  # Time manipulation mechanics
        }

        # Simple scenarios are more straightforward
        simple_scenarios = {
            ScenarioType.THE_GATHERING,  # Tutorial
            ScenarioType.THE_DEVOURER_BELOW,  # Direct boss fight
        }

        if self.scenario_type in complex_scenarios:
            return 0.7
        elif self.scenario_type in simple_scenarios:
            return 0.2
        else:
            return 0.4

    def _get_scenario_difficulty_modifier(self) -> float:
        """Get scenario-specific difficulty modifier"""
        # Inherently harder scenarios regardless of difficulty setting
        hard_scenarios = {
            ScenarioType.DIM_CARCOSA,
            ScenarioType.BEFORE_THE_BLACK_THRONE,
            ScenarioType.SHATTERED_AEONS,
        }

        # Easier scenarios
        easy_scenarios = {
            ScenarioType.THE_GATHERING,
            ScenarioType.EXTRACURRICULAR_ACTIVITIES,
        }

        if self.scenario_type in hard_scenarios:
            return 0.2
        elif self.scenario_type in easy_scenarios:
            return -0.2
        else:
            return 0.0
