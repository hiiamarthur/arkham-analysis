"""
Main Scenario Class - Coordinates all components and provides unified interface
Acts as the orchestrator following the Facade pattern
"""

from abc import ABC
from typing import Dict, List, Any, Optional

import sys
import os

from domain.card import EncounterCard

backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
if backend_path not in sys.path:
    sys.path.append(backend_path)

from domain import ScenarioType, Difficulty, CampaignType
from domain.Token.chaos_bag import ChaosBag
from .components import (
    ChaosBagManager,
    ContextCalculator,
    ScenarioConfig,
    DifficultyModifier,
)


class Scenario(ABC):
    """
    Main Scenario coordination class that orchestrates all components
    Provides unified interface for scenario operations
    """

    def __init__(
        self,
        campaign_chaos_bag: ChaosBag,
        campaign_type: CampaignType,
        scenario_type: ScenarioType,
        difficulty: Difficulty,
        player_count: int,
        encounter_cards: List[EncounterCard],
    ):
        print("encounter_cards", encounter_cards)
        self.scenario_type = scenario_type
        self.difficulty = difficulty
        self.campaign_type = campaign_type
        self.player_count = player_count
        self._config = None

        # Initialize components (Composition pattern)
        # self.config = ScenarioConfig(scenario_type, difficulty, player_count)
        # self.config = None
        self.chaos_manager = ChaosBagManager(
            campaign_chaos_bag, scenario_type, difficulty
        )
        self.context_calculator = ContextCalculator(
            scenario_type, difficulty, player_count
        )
        self.difficulty_modifier = DifficultyModifier(difficulty)

        # Apply initial setup
        self._initialize_scenario()
        self.encounter_cards = encounter_cards

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert scenario to dictionary with selective serialization.
        Only includes relevant data for API responses and persistence.
        """
        return {
            # Basic scenario identification
            "scenario_type": self.scenario_type.value,
            "difficulty": self.difficulty.value,
            "campaign_type": self.campaign_type.value,
            "player_count": self.player_count,
            # Calculated scenario values from rules
            "doom_threshold": self.doom_threshold,
            "starting_clues": self.starting_clues,
            "agenda_advancement_rate": self.agenda_advancement_rate,
            # Dynamic context metrics
            "scenario_context": self.get_scenario_context(),
            # Chaos bag analysis
            "chaos_bag_stats": self.get_chaos_bag_summary(),
            # Special mechanics and features
            "special_mechanics": self.special_mechanics,
            # Configuration summary (with enum serialization)
            "configuration": self._serialize_config_summary(),
            # Rule-calculated values from context calculator (with serialization)
            "rule_calculated_values": self._serialize_context_values(),
            # Scenario characteristics
            "is_time_pressured": self.is_time_pressured(),
            "is_investigation_heavy": self.is_investigation_heavy(),
            "is_combat_heavy": self.is_combat_heavy(),
            # Difficulty metrics
            "difficulty_multiplier": self.get_difficulty_multiplier(),
            "encounter_difficulty": self.calculate_encounter_difficulty(),
            # Resource analysis
            "time_pressure": self.calculate_time_pressure(),
            "resource_scarcity": self.calculate_resource_scarcity(),
            "encounter_cards": [card.dict for card in self.encounter_cards],
        }

    def _serialize_config_summary(self) -> Dict[str, Any]:
        """Serialize configuration with proper enum handling"""
        config = self.config.get_configuration_summary()
        return {
            "scenario_type": config["scenario_type"].value,
            "difficulty": config["difficulty"].value,
            "player_count": config["player_count"],
            "doom_threshold": config["doom_threshold"],
            "starting_clues": config["starting_clues"],
            "agenda_advancement_rate": config["agenda_advancement_rate"],
            "victory_points_required": config["victory_points_required"],
            "special_mechanics": config["special_mechanics"],
            "recommended_cards": config["recommended_cards"],
        }

    def _serialize_context_values(self) -> Dict[str, Any]:
        """Serialize context values with proper key handling for JSON"""

        def serialize_recursive(obj) -> Any:
            if isinstance(obj, dict):
                result: Dict[str, Any] = {}
                for key, value in obj.items():
                    # Convert tuple keys to string representation
                    if isinstance(key, tuple):
                        key = f"{key[0]}_{key[1]}"  # ('easy', 'standard') -> 'easy_standard'
                    elif hasattr(key, "value"):  # Handle enum keys
                        key = key.value
                    result[str(key)] = serialize_recursive(value)
                return result
            elif isinstance(obj, (list, tuple)):
                return [serialize_recursive(item) for item in obj]
            elif hasattr(obj, "value"):  # Handle enum values
                return obj.value
            else:
                return obj

        result = serialize_recursive(self.context_calculator.get_scenario_values())
        return result if isinstance(result, dict) else {}

    @property
    def config(self):
        if self._config is None:
            self._config = ScenarioConfig(self)
        return self._config

    def _initialize_scenario(self) -> None:
        """Initialize scenario with all component setup"""
        # Apply chaos bag modifications
        self.chaos_manager.apply_scenario_modifications()

        # Apply difficulty modifiers to config values
        self.config.doom_threshold = self.difficulty_modifier.apply_doom_modifier(
            self.config.doom_threshold
        )

    # =============================================================================
    # Main Scenario Interface Methods
    # =============================================================================

    def get_scenario_context(self) -> Dict[str, float]:
        """Get comprehensive scenario context for card evaluation"""
        return self.context_calculator.calculate_full_context(
            doom_threshold=self.config.doom_threshold,
            starting_clues=self.config.starting_clues,
            agenda_rate=self.config.agenda_advancement_rate,
            chaos_bag=self.chaos_manager.chaos_bag,
            player_count=self.player_count,
        )

    def get_initial_context_values(self) -> Dict[str, Any]:
        """Get initial context values for scenario setup"""
        return {
            **self.config.get_configuration_summary(),
            "context_metrics": self.get_scenario_context(),
            "chaos_bag_stats": self.get_chaos_bag_summary(),
        }

    def get_chaos_bag_summary(self) -> Dict[str, Any]:
        """Get chaos bag analysis summary"""
        return {
            "expected_value": self.chaos_manager.get_expected_value(),
            "hostility_rating": self.chaos_manager.get_hostility_rating(),
            "composition": self.chaos_manager.get_chaos_bag_composition(),
            "simulation_ready": True,
        }

    # =============================================================================
    # Chaos Bag Simulation Methods (Delegation to ChaosBagManager)
    # =============================================================================

    def simulate_chaos_draws(self, iterations: int = 1000) -> Dict[str, Any]:
        """Simulate chaos bag draws with statistical analysis"""
        return self.chaos_manager.simulate_draws(iterations)

    def calculate_success_probability(
        self, skill_value: int, target_difficulty: int
    ) -> float:
        """Calculate success probability for a skill test"""
        return self.chaos_manager.calculate_success_probability(
            target_difficulty, skill_value
        )

    def analyze_chaos_variance(self) -> Dict[str, float]:
        """Analyze statistical variance in chaos bag"""
        simulation_data = self.simulate_chaos_draws(5000)

        return {
            "mean_modifier": simulation_data["mean_value"],
            "standard_deviation": simulation_data["std_dev"],
            "variance": (
                simulation_data["std_dev"] ** 2 if simulation_data["std_dev"] > 0 else 0
            ),
            "consistency_rating": self._calculate_consistency_rating(
                simulation_data["std_dev"]
            ),
        }

    # =============================================================================
    # Context Analysis Methods (Delegation to ContextCalculator)
    # =============================================================================

    def calculate_time_pressure(self) -> float:
        """Calculate time pressure for this scenario"""
        return self.context_calculator.calculate_time_pressure(
            self.config.doom_threshold,
            self.config.agenda_advancement_rate,
            self.player_count,
        )

    def calculate_resource_scarcity(self) -> float:
        """Calculate resource scarcity for this scenario"""
        return self.context_calculator.calculate_resource_scarcity(
            self.config.starting_clues, self.player_count
        )

    def calculate_encounter_difficulty(self) -> float:
        """Calculate overall encounter difficulty"""
        return self.context_calculator.calculate_encounter_difficulty()

    # =============================================================================
    # Configuration Access Methods (Delegation to ScenarioConfig)
    # =============================================================================

    @property
    def doom_threshold(self) -> int:
        """Get doom threshold for this scenario"""
        return self.config.doom_threshold

    @property
    def starting_clues(self) -> int:
        """Get starting clues for this scenario"""
        return self.config.starting_clues

    @property
    def agenda_advancement_rate(self) -> float:
        """Get agenda advancement rate"""
        return self.config.agenda_advancement_rate

    @property
    def special_mechanics(self) -> Dict[str, Any]:
        """Get scenario-specific mechanics"""
        return self.config.special_mechanics

    def is_time_pressured(self) -> bool:
        """Check if scenario has significant time pressure"""
        return self.config.is_time_pressured()

    def is_investigation_heavy(self) -> bool:
        """Check if scenario is investigation-focused"""
        return self.config.is_investigation_heavy()

    def is_combat_heavy(self) -> bool:
        """Check if scenario is combat-focused"""
        return self.config.is_combat_heavy()

    # =============================================================================
    # Difficulty Modifier Methods (Delegation to DifficultyModifier)
    # =============================================================================

    def get_card_value_modifier(self, card_type: str) -> float:
        """Get difficulty-based card value modifier"""
        return self.difficulty_modifier.get_card_value_modifier(card_type)

    def get_difficulty_multiplier(self) -> float:
        """Get overall difficulty multiplier"""
        return self.config.get_difficulty_multiplier()

    # =============================================================================
    # Advanced Analysis Methods (Scenario-level coordination)
    # =============================================================================

    def evaluate_scenario_suitability_for_deck(
        self, deck_archetype: str
    ) -> Dict[str, Any]:
        """Evaluate how suitable this scenario is for a given deck archetype"""
        context = self.get_scenario_context()

        # Define archetype preferences (this could be expanded significantly)
        archetype_preferences = {
            "combat_heavy": {
                "time_pressure": -0.2,  # Combat decks prefer less time pressure
                "resource_scarcity": 0.1,  # Can handle some resource constraints
                "chaos_hostility": 0.0,  # Neutral to chaos bag hostility
            },
            "investigation": {
                "time_pressure": -0.3,  # Investigation needs time
                "resource_scarcity": -0.2,  # Needs resources for tools
                "chaos_hostility": -0.1,  # Prefers reliable skill tests
            },
            "support": {
                "time_pressure": 0.1,  # Support can help with time pressure
                "resource_scarcity": 0.2,  # Support helps with resources
                "chaos_hostility": 0.1,  # Support can mitigate chaos
            },
            "balanced": {
                "time_pressure": 0.0,  # Neutral preferences
                "resource_scarcity": 0.0,
                "chaos_hostility": 0.0,
            },
        }

        preferences = archetype_preferences.get(
            deck_archetype, archetype_preferences["balanced"]
        )

        suitability_score = 0.5  # Base neutral score
        for factor, weight in preferences.items():
            context_value = context.get(factor, 0.5)
            # Positive weight means archetype benefits from high context value
            # Negative weight means archetype suffers from high context value
            suitability_score += (context_value - 0.5) * weight

        return {
            "suitability_score": max(0.0, min(1.0, suitability_score)),
            "scenario_context": context,
            "archetype_preferences": preferences,
            "recommended": suitability_score > 0.6,
        }

    def get_recommended_player_strategies(self) -> Dict[str, List[str]]:
        """Get recommended strategies based on scenario characteristics"""
        strategies = {
            "general": ["Balanced approach", "Team coordination"],
            "combat": [],
            "investigation": [],
            "survival": [],
            "economy": [],
        }

        context = self.get_scenario_context()

        # Add specific strategies based on context
        if context["time_pressure"] > 0.7:
            strategies["general"].append("Prioritize speed over efficiency")
            strategies["economy"].append("Invest in action economy")

        if context["resource_scarcity"] > 0.6:
            strategies["economy"].extend(
                ["Conservative resource usage", "Prioritize free actions"]
            )

        if context["chaos_hostility"] > 0.7:
            strategies["general"].append("Focus on skill test mitigation")
            strategies["survival"].append("Pack extra skill boost cards")

        if self.is_combat_heavy():
            strategies["combat"].extend(["High damage weapons", "Combat support cards"])

        if self.is_investigation_heavy():
            strategies["investigation"].extend(
                ["Investigation tools", "Clue acceleration"]
            )

        return strategies

    def _calculate_consistency_rating(self, std_dev: float) -> float:
        """Calculate chaos bag consistency rating"""
        if std_dev == 0:
            return 1.0

        max_reasonable_std = 3.0
        consistency = max(0.0, 1.0 - (std_dev / max_reasonable_std))
        return min(1.0, consistency)

    # =============================================================================
    # Validation and Utility Methods
    # =============================================================================

    def validate_scenario_setup(self) -> List[str]:
        """Validate scenario configuration"""
        errors = []

        if self.doom_threshold < 1:
            errors.append("Invalid doom threshold")

        if self.starting_clues < 1:
            errors.append("Invalid starting clues")

        if self.agenda_advancement_rate <= 0:
            errors.append("Invalid agenda advancement rate")

        if not self.chaos_manager._modifications_applied:
            errors.append("Chaos bag modifications not applied")

        return errors

    def __str__(self) -> str:
        return f"Scenario({self.scenario_type.value}, {self.difficulty.value})"

    def __repr__(self) -> str:
        return (
            f"Scenario(scenario_type={self.scenario_type}, "
            f"difficulty={self.difficulty}, "
            f"doom_threshold={self.doom_threshold}, "
            f"starting_clues={self.starting_clues})"
        )
