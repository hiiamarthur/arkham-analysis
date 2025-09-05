"""
Edge of the Earth Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


EDGE_OF_THE_EARTH_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.ICE_AND_DEATH: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Antarctic expedition begins
            LocationSetupRule(
                required_locations=[
                    "arkham_station",
                    "train_car",
                    "miskatonic_university",
                ],
            ),
            # Introduction to Antarctic setting
            DynamicValueRule("antarctic_expedition", lambda ctx: True),
            DynamicValueRule("cold_mechanics", lambda ctx: True),
            # Tekelili creatures
            DynamicValueRule("tekelili_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-1. If it is Act 2 or higher, -3 instead.",
                            "value": -1,
                        },
                        ("hard", "expert"): {
                            "effect": "-2. If it is Act 2 or higher, -4 instead.",
                            "value": -2,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.FATAL_MIRAGE: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Desert mirage scenario
            LocationSetupRule(
                required_locations=["desert_outpost", "mirage_oasis", "sand_dunes"],
            ),
            # Mirage mechanics
            DynamicValueRule("mirage_mechanics", lambda ctx: True),
            DynamicValueRule("desert_exploration", lambda ctx: True),
            DynamicValueRule("heat_exposure", lambda ctx: True),
            # Partner mechanics
            DynamicValueRule("partner_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are at a Mirage location, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are at a Mirage location, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.TO_THE_FORBIDDEN_PEAKS: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Mountain climbing scenario
            LocationSetupRule(
                required_locations=["base_camp", "precarious_path", "mountain_peak"],
            ),
            # Elevation and climbing mechanics
            DynamicValueRule("elevation_mechanics", lambda ctx: True),
            DynamicValueRule("mountain_climbing", lambda ctx: True),
            DynamicValueRule("cold_exposure", lambda ctx: True),
            # Partner mechanics
            DynamicValueRule("partner_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are at an Elevated location, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are at an Elevated location, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.CITY_OF_THE_ELDER_THINGS: [
            PlayerCountScalingRule("starting_clues", 4, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # Ancient alien city
            LocationSetupRule(
                required_locations=[
                    "elder_thing_city",
                    "specimen_storage",
                    "laboratory",
                ],
            ),
            # Elder Thing mechanics
            DynamicValueRule("elder_thing_mechanics", lambda ctx: True),
            DynamicValueRule("alien_technology", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Ancient city exploration
            DynamicValueRule("exploration_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are fewer than 3 clues on locations, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If there are fewer than 4 clues on locations, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_HEART_OF_MADNESS: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 12 + ctx["player_count"]),
            # Campaign finale in the deep
            LocationSetupRule(
                required_locations=[
                    "the_heart_of_madness",
                    "shoggoth_lair",
                    "primordial_depths",
                ],
            ),
            # Campaign finale
            DynamicValueRule("campaign_finale", lambda ctx: True),
            DynamicValueRule("boss_fight", lambda ctx: True),
            DynamicValueRule("shoggoth_mechanics", lambda ctx: True),
            # Heart of madness
            DynamicValueRule("madness_finale", lambda ctx: True),
            # Multi-part scenario mechanics
            DynamicValueRule("multi_part_scenario", lambda ctx: True),
            DynamicValueRule("underground_exploration", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-4. If this skill test fails, place 1 doom on the current agenda.",
                            "value": -4,
                        },
                        ("hard", "expert"): {
                            "effect": "-6. If this skill test fails, place 1 doom on the current agenda.",
                            "value": -6,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
