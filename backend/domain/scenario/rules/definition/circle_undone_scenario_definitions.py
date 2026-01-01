"""
Circle Undone Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


CIRCLE_UNDONE_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.DISAPPEARANCE_AT_THE_TWLIGHT_ESTATE: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Hospital setting
            LocationSetupRule(
                required_locations=[
                    "arkham_sanatorium",
                    "patient_confinement",
                    "basement",
                ],
            ),
        ],
        ScenarioType.AT_DEATHS_DOORSTEP: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Hospital setting
            LocationSetupRule(
                required_locations=[
                    "arkham_sanatorium",
                    "patient_confinement",
                    "basement",
                ],
            ),
        ],
        ScenarioType.THE_WITCHING_HOUR: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Witchcraft and Salem setting
            LocationSetupRule(
                required_locations=[
                    "your_house",
                    "silver_twilight_lodge",
                    "french_hill",
                ],
                optional_locations=[
                    "witch_house_ruins",
                    "hangmans_hill",
                    "arkham_woods",
                ],
            ),
            # Witch mechanics introduction
            DynamicValueRule("witch_mechanics", lambda ctx: True),
            DynamicValueRule("salem_setting", lambda ctx: True),
            # Spectral mechanics
            DynamicValueRule("spectral_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-1. If you fail, place 1 doom on your investigator.",
                            "value": -1,
                        },
                        ("hard", "expert"): {
                            "effect": "-2. If you fail, place 1 doom on your investigator.",
                            "value": -2,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.AT_DEATHS_DOORSTEP: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Hospital setting
            LocationSetupRule(
                required_locations=[
                    "arkham_sanatorium",
                    "patient_confinement",
                    "basement",
                ],
            ),
            # Death and resurrection themes
            DynamicValueRule("death_mechanics", lambda ctx: True),
            DynamicValueRule("hospital_setting", lambda ctx: True),
            # Spectral encounters
            DynamicValueRule("spectral_encounters", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are 4 or more horror tokens among investigators at your location, you automatically fail.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If there are 3 or more horror tokens among investigators at your location, you automatically fail.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_SECRET_NAME: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Lodge investigation
            LocationSetupRule(
                required_locations=[
                    "silver_twilight_lodge",
                    "lodge_gates",
                    "lodge_catacombs",
                ],
            ),
            # Secret society mechanics
            DynamicValueRule("lodge_mechanics", lambda ctx: True),
            DynamicValueRule("secret_society", lambda ctx: True),
            # Witch and lodge conflict
            DynamicValueRule("witch_lodge_conflict", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are fewer than 4 cards in your hand, you automatically fail.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If there are fewer than 4 cards in your hand, you automatically fail.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_WAGES_OF_SIN: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Hangman's Hill investigation
            LocationSetupRule(
                required_locations=[
                    "hangmans_hill",
                    "abandoned_chapel",
                    "heretics_graves",
                ],
            ),
            # Heretic mechanics
            DynamicValueRule("heretic_mechanics", lambda ctx: True),
            DynamicValueRule("wage_of_sin", lambda ctx: True),
            # Keziah Mason investigation
            DynamicValueRule("keziah_mason", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are at Hangman's Hill, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are at Hangman's Hill, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.FOR_THE_GREATER_GOOD: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Lodge infiltration
            LocationSetupRule(
                required_locations=["lodge_sanctum", "lodge_library", "inner_sanctum"],
            ),
            # Moral choice mechanics
            DynamicValueRule("moral_choices", lambda ctx: True),
            DynamicValueRule("lodge_infiltration", lambda ctx: True),
            # Carl Sanford confrontation
            DynamicValueRule("carl_sanford", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you have taken no damage or horror this scenario, -5 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you have taken no damage or horror this scenario, -7 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.UNION_AND_DISILLUSION: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # Miskatonic University showdown
            LocationSetupRule(
                required_locations=[
                    "miskatonic_university",
                    "administration_building",
                    "orne_library",
                ],
            ),
            # Union of witch and lodge power
            DynamicValueRule("union_mechanics", lambda ctx: True),
            DynamicValueRule("university_showdown", lambda ctx: True),
            # Anette Mason finale
            DynamicValueRule("anette_mason_finale", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-4. If there are Spectral enemies in play, -6 instead.",
                            "value": -4,
                        },
                        ("hard", "expert"): {
                            "effect": "-5. If there are Spectral enemies in play, -8 instead.",
                            "value": -5,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.IN_THE_CLUTCHES_OF_CHAOS: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # French Hill chaos
            LocationSetupRule(
                required_locations=["french_hill", "unvisited_isle", "the_witch_house"],
            ),
            # Chaos and madness mechanics
            DynamicValueRule("chaos_mechanics", lambda ctx: True),
            DynamicValueRule("mass_hysteria", lambda ctx: True),
            # Witch House investigation
            DynamicValueRule("witch_house_mechanics", lambda ctx: True),
            TimeBasedRule(rounds_limit=None, doom_per_round=1.3),  # High pressure
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If there are 4 or more doom tokens in play, -6 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If there are 3 or more doom tokens in play, -8 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.BEFORE_THE_BLACK_THRONE: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 13 + ctx["player_count"]),
            # Campaign finale in cosmic realm
            LocationSetupRule(
                required_locations=["cosmic_gate", "black_throne", "azathoths_realm"],
            ),
            # Campaign finale
            DynamicValueRule("campaign_finale", lambda ctx: True),
            DynamicValueRule("boss_fight", lambda ctx: True),
            DynamicValueRule("azathoth_mechanics", lambda ctx: True),
            # Black Throne confrontation
            DynamicValueRule("black_throne_mechanics", lambda ctx: True),
            # Multiple resolution paths
            DynamicValueRule("multiple_resolutions", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-5. If this skill test fails, place 2 doom on the current agenda.",
                            "value": -5,
                        },
                        ("hard", "expert"): {
                            "effect": "-7. If this skill test fails, place 3 doom on the current agenda.",
                            "value": -7,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
