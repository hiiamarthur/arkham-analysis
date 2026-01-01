"""
Dunwich Legacy Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


DUNWICH_LEGACY_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.EXTRACURRICULAR_ACTIVITY: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # University setting
            LocationSetupRule(
                required_locations=[
                    "miskatonic_quad",
                    "humanities_building",
                    "science_building",
                    "administration_building",
                ],
            ),
            # Students and faculty mechanics
            DynamicValueRule(
                "faculty_offices", lambda ctx: 4
            ),  # 4 random faculty offices
            DynamicValueRule("student_unions", lambda ctx: 2),  # 2 student unions
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are at a Faculty Office location, you automatically fail.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are at a Faculty Office location, you automatically fail.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_HOUSE_ALWAYS_WINS: [
            PlayerCountScalingRule("starting_clues", 1, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 7 + ctx["player_count"]),
            # Casino setting
            LocationSetupRule(
                required_locations=[
                    "clover_club_lounge",
                    "clover_club_bar",
                    "clover_club_cardroom",
                ],
            ),
            # Gambling and money mechanics
            DynamicValueRule(
                "starting_resources", lambda ctx: 10
            ),  # Start with extra resources
            DynamicValueRule("gambling_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. You may spend 3 resources to treat this token as a 0 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. You may spend 4 resources to treat this token as a 0 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_MISKATONIC_MUSEUM: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Museum layout
            LocationSetupRule(
                required_locations=[
                    "museum_entrance",
                    "museum_halls",
                    "administration_office",
                    "security_office",
                ],
                optional_locations=[
                    "restricted_hall",
                    "exhibit_hall_athabaskan",
                    "exhibit_hall_medieval",
                    "exhibit_hall_egyptian",
                ],
            ),
            # Night watchman and security mechanics
            DynamicValueRule("night_watchman", lambda ctx: True),
            DynamicValueRule("security_level", lambda ctx: 3),  # 3 levels of security
            # Investigation heavy
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-1. If you are in a Restricted location, -3 instead.",
                            "value": -1,
                        },
                        ("hard", "expert"): {
                            "effect": "-2. If you are in a Restricted location, -4 instead.",
                            "value": -2,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_ESSEX_COUNTRY_EXPRESS: [
            PlayerCountScalingRule("starting_clues", 1, per_player=1),
            DynamicValueRule(
                "doom_threshold", lambda ctx: 6 + ctx["player_count"]
            ),  # Shorter scenario
            # Moving train mechanics
            TimeBasedRule(rounds_limit=None, doom_per_round=1.2),  # Accelerated doom
            DynamicValueRule("moving_train", lambda ctx: True),
            # Train car progression
            LocationSetupRule(
                required_locations=[
                    "engine_car",
                    "passenger_car",
                    "dining_car",
                    "parlor_car",
                ],
            ),
            DynamicValueRule("car_advancement", lambda ctx: True),
            DynamicValueRule("time_pressure", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-X. X is the current Agenda number.",
                            "value": "X",
                        },
                        ("hard", "expert"): {
                            "effect": "-X. X is twice the current Agenda number.",
                            "value": "2X",
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.BLOOD_ON_THE_ALTAR: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Kidnapped allies mechanic
            DynamicValueRule("kidnapped_allies", lambda ctx: True),
            # Village locations
            LocationSetupRule(
                required_locations=[
                    "village_commons",
                    "dunwich_general_store",
                    "bishops_brook",
                ],
                optional_locations=[
                    "cold_spring_glen",
                    "tenebrous_path",
                    "the_hidden_chamber",
                ],
            ),
            # Sacrifice and rescue mechanics
            DynamicValueRule("rescue_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are no Kidnapped allies in play, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If there are no Kidnapped allies in play, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.UNDIMENSIONED_AND_UNSEEN: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule(
                "doom_threshold", lambda ctx: 12 + ctx["player_count"]
            ),  # Longer scenario
            # Multiple Dunwich Horror spawns
            DynamicValueRule(
                "dunwich_horrors", lambda ctx: min(ctx["player_count"] + 1, 4)
            ),
            DynamicValueRule("large_scenario", lambda ctx: True),
            # Dunwich countryside
            LocationSetupRule(
                required_locations=[
                    "dunwich_village",
                    "cold_spring_glen",
                    "tenebrous_path",
                    "devils_hop_yard",
                ],
            ),
            # Brood of Yog-Sothoth mechanics
            DynamicValueRule("brood_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-X. X is the number of Dunwich Horror enemies in play.",
                            "value": "X",
                        },
                        ("hard", "expert"): {
                            "effect": "-X. X is twice the number of Dunwich Horror enemies in play.",
                            "value": "2X",
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.WHERE_DOOM_AWAITS: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Sentinel Hill climb
            LocationSetupRule(
                required_locations=[
                    "base_of_the_hill",
                    "ascending_path",
                    "sentinel_hill",
                ],
            ),
            # Climbing mechanics
            DynamicValueRule("climbing_mechanics", lambda ctx: True),
            DynamicValueRule("altitude_effects", lambda ctx: True),
            # Yog-Sothoth summoning
            DynamicValueRule("yog_sothoth_summoning", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are not at Sentinel Hill, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are not at Sentinel Hill, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.LOST_IN_TIME_AND_SPACE: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # Otherworldly locations
            LocationSetupRule(
                required_locations=[
                    "another_dimension",
                    "the_edge_of_the_universe",
                    "tear_through_space",
                ],
            ),
            # Space-time mechanics
            DynamicValueRule("spacetime_mechanics", lambda ctx: True),
            DynamicValueRule("extradimensional", lambda ctx: True),
            # Final campaign scenario
            DynamicValueRule("campaign_finale", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you fail, lose 1 action.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-5. If you fail, lose 2 actions.",
                            "value": -5,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
