"""
Scenario Configuration - Manages scenario-specific data and settings
Follows SRP by focusing solely on configuration management
"""

from typing import Dict, Optional, Any

import sys
import os

backend_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."
)
if backend_path not in sys.path:
    sys.path.append(backend_path)

from typing import TYPE_CHECKING
from domain import ScenarioType, Difficulty

if TYPE_CHECKING:
    from ..scenario import Scenario


class ScenarioConfig:
    """Manages scenario-specific configuration data and calculations"""

    def __init__(self, scenario: "Scenario"):
        self.scenario_type = scenario.scenario_type
        self.difficulty = scenario.difficulty
        self.player_count = scenario.player_count

        # Load configuration on initialization
        self._load_configuration()

    def _load_configuration(self) -> None:
        """Load all scenario configuration values"""
        self.doom_threshold = self._calculate_doom_threshold()
        self.starting_clues = self._calculate_starting_clues()
        self.agenda_advancement_rate = self._calculate_agenda_rate()
        self.victory_points_required = self._calculate_victory_points()
        self.special_mechanics = self._get_special_mechanics()
        self.recommended_player_cards = self._get_recommended_cards()

    def _calculate_doom_threshold(self) -> int:
        """Calculate doom threshold for this scenario and difficulty"""
        # Base doom threshold varies by scenario
        scenario_doom_map = {
            # Night of the Zealot
            ScenarioType.THE_GATHERING: 7,
            ScenarioType.THE_MIDNIGHT_MASKS: 9,
            ScenarioType.THE_DEVOURER_BELOW: 10,
            # Dunwich Legacy
            ScenarioType.EXTRACURRICULAR_ACTIVITIES: 8,
            ScenarioType.THE_HOUSE_ALWAYS_WINS: 7,
            ScenarioType.THE_MISKATONIC_MUSEUM: 9,
            ScenarioType.THE_ESSEX_COUNTRY_EXPRESS: 6,  # Fast-paced scenario
            ScenarioType.BLOOD_ON_THE_ALTAR: 8,
            ScenarioType.UNDIMENSIONED_AND_UNSEEN: 12,  # Long scenario
            ScenarioType.WHERE_DOOM_AWAITS: 9,
            ScenarioType.LOST_IN_TIME_AND_SPACE: 11,
            # Path to Carcosa
            ScenarioType.CURTAIN_CALLS: 8,
            ScenarioType.THE_LAST_KING: 10,
            ScenarioType.ECHO_OF_THE_PAST: 7,
            ScenarioType.THE_UNSPEAKABLE_OATH: 9,
            ScenarioType.A_PHANTOM_OF_TRUTH: 8,
            ScenarioType.THE_PALLID_MASK: 11,
            ScenarioType.BLACK_STAR_RISE: 9,
            ScenarioType.DIM_CARCOSA: 12,  # Final scenario
        }

        base_doom = scenario_doom_map.get(self.scenario_type, 8)  # Default 8

        # Difficulty adjustments
        difficulty_modifiers = {
            Difficulty.EASY: +2,
            Difficulty.STANDARD: 0,
            Difficulty.HARD: -1,
            Difficulty.EXPERT: -2,
        }

        # Player count adjustments (more players = slightly more doom)
        player_modifier = max(0, self.player_count - 2)  # +1 doom per player above 2

        final_doom = (
            base_doom + difficulty_modifiers.get(self.difficulty, 0) + player_modifier
        )
        return max(5, final_doom)  # Minimum 5 doom threshold

    def _calculate_starting_clues(self) -> int:
        """Calculate starting clues based on scenario and player count"""
        # Base clues per scenario (for 2 players)
        scenario_clues_map = {
            # Night of the Zealot
            ScenarioType.THE_GATHERING: 4,
            ScenarioType.THE_MIDNIGHT_MASKS: 6,
            ScenarioType.THE_DEVOURER_BELOW: 5,
            # Dunwich Legacy
            ScenarioType.EXTRACURRICULAR_ACTIVITIES: 5,
            ScenarioType.THE_HOUSE_ALWAYS_WINS: 4,
            ScenarioType.THE_MISKATONIC_MUSEUM: 7,  # Investigation heavy
            ScenarioType.THE_ESSEX_COUNTRY_EXPRESS: 3,  # Action heavy
            ScenarioType.BLOOD_ON_THE_ALTAR: 6,
            ScenarioType.UNDIMENSIONED_AND_UNSEEN: 8,  # Large scenario
            ScenarioType.WHERE_DOOM_AWAITS: 5,
            ScenarioType.LOST_IN_TIME_AND_SPACE: 7,
            # Path to Carcosa
            ScenarioType.CURTAIN_CALLS: 4,
            ScenarioType.THE_LAST_KING: 6,
            ScenarioType.ECHO_OF_THE_PAST: 5,
            ScenarioType.THE_UNSPEAKABLE_OATH: 4,
            ScenarioType.A_PHANTOM_OF_TRUTH: 6,
            ScenarioType.THE_PALLID_MASK: 8,  # Complex investigation
            ScenarioType.BLACK_STAR_RISE: 5,
            ScenarioType.DIM_CARCOSA: 7,
        }

        base_clues = scenario_clues_map.get(self.scenario_type, 4)

        # Scale with player count (roughly +1 clue per additional player)
        player_scaling = max(0, self.player_count - 2)

        return base_clues + player_scaling

    def _calculate_agenda_rate(self) -> float:
        """Calculate agenda advancement rate (doom per round)"""
        # Most scenarios advance 1 doom per round
        standard_rate = 1.0

        # Fast scenarios with accelerated doom
        fast_scenarios = {
            ScenarioType.THE_MIDNIGHT_MASKS: 1.3,  # Time pressure
            ScenarioType.THE_DEVOURER_BELOW: 1.2,  # Boss pressure
            ScenarioType.THE_ESSEX_COUNTRY_EXPRESS: 1.4,  # Moving train
        }

        # Slow scenarios with more time
        slow_scenarios = {
            ScenarioType.THE_GATHERING: 0.8,  # Tutorial pace
            ScenarioType.THE_MISKATONIC_MUSEUM: 0.9,  # Investigation focus
        }

        base_rate = fast_scenarios.get(
            self.scenario_type, slow_scenarios.get(self.scenario_type, standard_rate)
        )

        # Difficulty adjustments
        if self.difficulty in [Difficulty.HARD, Difficulty.EXPERT]:
            base_rate += 0.1  # Slightly faster on higher difficulties

        return base_rate

    def _calculate_victory_points(self) -> int:
        """Calculate required victory points to win scenario"""
        # Most scenarios require advancing through all acts
        scenario_vp_map = {
            ScenarioType.THE_GATHERING: 3,  # Simple scenario
            ScenarioType.THE_MIDNIGHT_MASKS: 4,
            ScenarioType.THE_DEVOURER_BELOW: 5,  # Boss scenario
            # Add more as needed
        }

        return scenario_vp_map.get(self.scenario_type, 4)  # Default 4 VP

    def _get_special_mechanics(self) -> Dict[str, Any]:
        """Get scenario-specific special mechanics"""
        mechanics = {
            ScenarioType.THE_GATHERING: {
                "ghoul_mechanics": True,
                "cellar_access": True,
            },
            ScenarioType.THE_MIDNIGHT_MASKS: {
                "time_limit": True,
                "cultist_hunting": True,
                "multiple_locations": True,
            },
            ScenarioType.THE_DEVOURER_BELOW: {
                "boss_fight": True,
                "umôrdhoth": True,
            },
            ScenarioType.THE_ESSEX_COUNTRY_EXPRESS: {
                "moving_train": True,
                "car_advancement": True,
            },
            ScenarioType.THE_PALLID_MASK: {
                "catacombs": True,
                "skull_mechanics": True,
                "complex_navigation": True,
            },
        }

        return mechanics.get(self.scenario_type, {})

    def _get_recommended_cards(self) -> Dict[str, list]:
        """Get recommended card types for this scenario"""
        recommendations = {
            ScenarioType.THE_GATHERING: {
                "combat_cards": ["weapons", "combat_events"],
                "investigation_cards": ["investigation_tools"],
                "survival_cards": ["healing", "sanity_protection"],
            },
            ScenarioType.THE_MIDNIGHT_MASKS: {
                "movement_cards": ["shortcut", "pathfinding"],
                "investigation_cards": ["clue_gathering", "location_control"],
                "efficiency_cards": ["action_economy"],
            },
            ScenarioType.THE_DEVOURER_BELOW: {
                "combat_cards": ["high_damage_weapons", "combat_buffs"],
                "survival_cards": ["damage_mitigation", "horror_protection"],
                "support_cards": ["team_buffs"],
            },
        }

        return recommendations.get(
            self.scenario_type, {"general_cards": ["balanced_deck", "flexibility"]}
        )

    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get complete configuration summary"""
        return {
            "scenario_type": self.scenario_type,
            "difficulty": self.difficulty,
            "player_count": self.player_count,
            "doom_threshold": self.doom_threshold,
            "starting_clues": self.starting_clues,
            "agenda_advancement_rate": self.agenda_advancement_rate,
            "victory_points_required": self.victory_points_required,
            "special_mechanics": self.special_mechanics,
            "recommended_cards": self.recommended_player_cards,
        }

    def is_time_pressured(self) -> bool:
        """Check if scenario has significant time pressure"""
        return self.agenda_advancement_rate > 1.1

    def is_investigation_heavy(self) -> bool:
        """Check if scenario is investigation-focused"""
        return self.starting_clues >= 6

    def is_combat_heavy(self) -> bool:
        """Check if scenario is combat-focused"""
        combat_scenarios = {
            ScenarioType.THE_DEVOURER_BELOW,
            ScenarioType.BLOOD_ON_THE_ALTAR,
            ScenarioType.DIM_CARCOSA,
        }
        return self.scenario_type in combat_scenarios

    def get_difficulty_multiplier(self) -> float:
        """Get overall difficulty multiplier for scoring adjustments"""
        base_multipliers = {
            Difficulty.EASY: 0.8,
            Difficulty.STANDARD: 1.0,
            Difficulty.HARD: 1.2,
            Difficulty.EXPERT: 1.4,
        }

        return base_multipliers.get(self.difficulty, 1.0)
