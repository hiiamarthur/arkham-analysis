"""
Scenario Factory - Creates scenarios with proper dependency injection
Follows DIP and Factory patterns for clean object creation
"""

from typing import Dict, Any, Type, Optional, List

import sys
import os

backend_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."
)
if backend_path not in sys.path:
    sys.path.append(backend_path)

from domain import ScenarioType, Difficulty, CampaignType
from domain.Token.chaos_bag import ChaosBag
from ..scenario import Scenario
from domain.card import EncounterCard


class ScenarioFactory:
    """Factory for creating Scenario instances with proper setup"""

    @staticmethod
    def create_scenario(
        campaign_chaos_bag: ChaosBag,
        campaign_type: CampaignType,
        scenario_type: ScenarioType,
        difficulty: Difficulty,
        player_count,
        encounter_cards: Optional[List[EncounterCard]] = [],
        **kwargs,
    ) -> Scenario:
        """
        Create a scenario instance with full configuration

        Args:
            campaign_chaos_bag: The campaign's chaos bag
            campaign_type: Which campaign this scenario belongs to
            scenario_type: Specific scenario to create
            difficulty: Difficulty level
            player_count: Number of players (affects scaling)
            **kwargs: Additional configuration options

        Returns:
            Configured Scenario instance
        """
        return Scenario(
            campaign_chaos_bag=campaign_chaos_bag,
            campaign_type=campaign_type,
            scenario_type=scenario_type,
            difficulty=difficulty,
            player_count=player_count,
            encounter_cards=encounter_cards or [],
        )

    @staticmethod
    def create_scenario_from_config(config: Dict[str, Any]) -> Scenario:
        """
        Create scenario from configuration dictionary

        Args:
            config: Dictionary containing scenario configuration
                   Required keys: chaos_bag, campaign_type, scenario_type, difficulty
                   Optional keys: player_count
        """
        required_keys = ["chaos_bag", "campaign_type", "scenario_type", "difficulty"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")

        return ScenarioFactory.create_scenario(
            campaign_chaos_bag=config["chaos_bag"],
            campaign_type=config["campaign_type"],
            scenario_type=config["scenario_type"],
            difficulty=config["difficulty"],
            player_count=config.get("player_count", 2),
        )

    @staticmethod
    def create_campaign_scenarios(
        campaign_chaos_bag: ChaosBag,
        campaign_type: CampaignType,
        difficulty: Difficulty,
        player_count,
    ) -> Dict[ScenarioType, Scenario]:
        """
        Create all scenarios for a given campaign

        Returns:
            Dictionary mapping scenario types to scenario instances
        """
        from domain.scenarios import get_scenarios_by_campaign

        scenarios = {}
        campaign_scenarios = get_scenarios_by_campaign(campaign_type)

        for scenario_type in campaign_scenarios:
            scenarios[scenario_type] = ScenarioFactory.create_scenario(
                campaign_chaos_bag=campaign_chaos_bag,
                campaign_type=campaign_type,
                scenario_type=scenario_type,
                difficulty=difficulty,
                player_count=player_count,
            )

        return scenarios

    @staticmethod
    def create_test_scenario(
        player_count: int = 2,
        scenario_type: ScenarioType = ScenarioType.THE_GATHERING,
        difficulty: Difficulty = Difficulty.STANDARD,
    ) -> Scenario:
        """
        Create a test scenario with minimal setup for testing/development

        Creates a basic chaos bag for testing purposes
        """
        from domain.Token.token import (
            ElderSignToken,
            AutoFailToken,
            PlusOneToken,
            ZeroToken,
            MinusOneToken,
            MinusTwoToken,
            SkullToken,
            CultistToken,
        )

        # Create basic test chaos bag
        test_tokens = [
            ElderSignToken(),
            AutoFailToken(),
            PlusOneToken(),
            ZeroToken(),
            ZeroToken(),
            MinusOneToken(),
            MinusOneToken(),
            MinusOneToken(),
            MinusTwoToken(),
            MinusTwoToken(),
            SkullToken("", -2),
            CultistToken("", -1),
        ]

        test_chaos_bag = ChaosBag(test_tokens)

        # Determine campaign type from scenario
        from domain.scenarios import get_scenario_campaign

        campaign_type = get_scenario_campaign(scenario_type)

        return ScenarioFactory.create_scenario(
            campaign_chaos_bag=test_chaos_bag,
            campaign_type=campaign_type,
            scenario_type=scenario_type,
            difficulty=difficulty,
            player_count=player_count,
        )

    @staticmethod
    def create_comparative_scenarios(
        base_scenario_type: ScenarioType,
        difficulties: list = [],
        player_counts: list = [],
    ) -> Dict[str, Scenario]:
        """
        Create multiple versions of the same scenario for comparison

        Args:
            base_scenario_type: The scenario to create variations of
            difficulties: List of difficulties to test (default: all)
            player_counts: List of player counts to test (default: [1,2,3,4])

        Returns:
            Dictionary with descriptive keys mapping to scenario instances
        """
        if difficulties is None:
            difficulties = [
                Difficulty.EASY,
                Difficulty.STANDARD,
                Difficulty.HARD,
                Difficulty.EXPERT,
            ]

        if player_counts is None:
            player_counts = [1, 2, 3, 4]

        scenarios = {}

        for difficulty in difficulties:
            for player_count in player_counts:
                key = f"{base_scenario_type.value}_{difficulty.value}_{player_count}p"
                scenarios[key] = ScenarioFactory.create_test_scenario(
                    player_count=player_count,
                    scenario_type=base_scenario_type,
                    difficulty=difficulty,
                )

        return scenarios
