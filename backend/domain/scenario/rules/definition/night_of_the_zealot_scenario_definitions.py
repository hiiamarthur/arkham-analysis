"""
Night of the Zealot Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


NIGHT_OF_THE_ZEALOT_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.THE_GATHERING: [
            # Basic setup with standard encounter sets
            PlayerCountScalingRule("starting_clues", 2, per_player=1, min_players=1),
            DynamicValueRule(
                "doom_threshold", lambda ctx: 7 + (ctx["player_count"] - 1)
            ),
            # Chaos bag modifications for tutorial scenario
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-X. X is the number of Ghoul enemies at your location.",
                            "value": "X",
                        },
                        ("hard", "expert"): {
                            "effect": "-2. If you fail, after this skill test, search the encounter deck for a Ghoul enemy and draw it.",
                            "value": -2,
                        },
                    },
                    "cultist": {
                        ("easy", "standard"): {
                            "effect": "-1. If you fail, take 1 horror.",
                            "value": -1,
                        },
                        ("hard", "expert"): {
                            "effect": "Reveal another token. If you fail, take 2 horror.",
                            "value": 0,
                        },
                    },
                }
            ),
            # Location setup
            LocationSetupRule(
                required_locations=["study", "hallway", "attic", "cellar"],
                optional_locations=[],
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_MIDNIGHT_MASKS: [
            # Time pressure scenario
            TimeBasedRule(
                rounds_limit=None, doom_per_round=1.0
            ),  # No hard limit but pressure
            PlayerCountScalingRule("starting_clues", 4, per_player=1),
            DynamicValueRule(
                "doom_threshold", lambda ctx: 9 + (ctx["player_count"] - 2)
            ),
            # Multiple location setup with choices
            LocationSetupRule(
                required_locations=["your_house", "rivertown"],
                optional_locations=[
                    "downtown",
                    "easttown",
                    "northside",
                    "southside",
                    "uptown",
                    "miskatonic_university",
                ],
                selection_count=4,  # Choose 4 of the optional locations
            ),
            # Special cultist hunting mechanic
            DynamicValueRule(
                "cultist_locations", lambda ctx: min(6, ctx["player_count"] + 2)
            ),
            DynamicValueRule("time_pressure", lambda ctx: True),
            # Chaos bag modifications
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-X. X is the highest number of doom on a Cultist enemy in play.",
                            "value": "X",
                        },
                        ("hard", "expert"): {
                            "effect": "-2. Place 1 doom on the nearest Cultist enemy.",
                            "value": -2,
                        },
                    },
                    "cultist": {
                        ("easy", "standard"): {
                            "effect": "-2. Place 1 doom on the nearest Cultist enemy.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. Place 2 doom on the nearest Cultist enemy.",
                            "value": -4,
                        },
                    },
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_DEVOURER_BELOW: [
            # Random encounter set selection (key mechanic)
            RandomEncounterSetRule(
                [
                    "agents_of_yog_sothoth",
                    "agents_of_shub_niggurath",
                    "agents_of_cthulhu",
                    "agents_of_hastur",
                ],
                count=1,
            ),
            # Dynamic doom based on chosen encounter set
            DynamicValueRule(
                "doom_threshold",
                lambda ctx: 10
                + (
                    2
                    if "agents_of_cthulhu" in ctx.get("active_encounter_sets", [])
                    else (
                        1
                        if "agents_of_hastur" in ctx.get("active_encounter_sets", [])
                        else 0
                    )
                ),
            ),
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            # Boss fight mechanics
            DynamicValueRule("boss_fight", lambda ctx: True),
            DynamicValueRule(
                "umordoth_health", lambda ctx: 15 + (ctx["player_count"] * 5)
            ),
            # Location conditional removal
            ConditionalLocationRule(
                locations=["your_house"],
                condition=lambda ctx: ctx.get("midnight_masks_resolution", "unknown")
                == "failed",
                action="remove",
            ),
            # Chaos bag modifications
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are 10 or more cards in your discard pile, you automatically fail.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If there are 10 or more cards in your discard pile, you automatically fail.",
                            "value": -4,
                        },
                    },
                    "cultist": {
                        ("easy", "standard"): {
                            "effect": "-3. If you fail, place 1 doom on the current agenda.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-6. If you fail, place 1 doom on the current agenda.",
                            "value": -6,
                        },
                    },
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
