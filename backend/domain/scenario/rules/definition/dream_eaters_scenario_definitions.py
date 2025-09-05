"""
Dream Eaters Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


DREAM_EATERS_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.BEYOND_THE_GATE_OF_SLEEP: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Dream investigation setup
            LocationSetupRule(
                required_locations=[
                    "your_house_first_floor",
                    "your_house_second_floor",
                    "your_house_attic",
                    "the_enchanted_woods",
                ],
            ),
            # Dream/reality mechanics
            DynamicValueRule("dream_reality_split", lambda ctx: True),
            DynamicValueRule("zoogs_encounter", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-1. If you are in a Dream location, -3 instead.",
                            "value": -1,
                        },
                        ("hard", "expert"): {
                            "effect": "-2. If you are in a Dream location, -4 instead.",
                            "value": -2,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.WAKING_NIGHTMARE: [
            PlayerCountScalingRule("starting_clues", 1, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 7 + ctx["player_count"]),
            # Hospital setting
            LocationSetupRule(
                required_locations=[
                    "emergency_room",
                    "hospital_basement",
                    "records_office",
                    "experimental_therapies_ward",
                ],
            ),
            # Nightmare and madness mechanics
            DynamicValueRule("nightmare_mechanics", lambda ctx: True),
            DynamicValueRule("madness_accumulation", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you have 3+ horror, you automatically fail.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you have 2+ horror, you automatically fail.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_SEARCH_FOR_KADATH: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Dreamlands exploration
            LocationSetupRule(
                required_locations=[
                    "ulthar",
                    "dylath_leen",
                    "ilek_vad",
                    "the_silver_key",
                ],
                optional_locations=[
                    "celephas",
                    "temple_of_the_cats",
                    "the_cavern_of_flame",
                ],
            ),
            # Cats of Ulthar and dreamlands mechanics
            DynamicValueRule("cats_of_ulthar", lambda ctx: True),
            DynamicValueRule("dreamlands_travel", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-1. If you control a Cat ally, treat this as a 0.",
                            "value": -1,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you control a Cat ally, -1 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.A_THOUSAND_SHAPES_OF_HORROR: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 6 + ctx["player_count"]),
            # Nyarlathotep shapes mechanic
            LocationSetupRule(
                required_locations=[
                    "streets_of_cairo",
                    "the_cairo_museum",
                    "old_cairo",
                ],
            ),
            # Shape-changing enemy mechanics
            DynamicValueRule("nyarlathotep_shapes", lambda ctx: 3),
            DynamicValueRule("shape_transformation", lambda ctx: True),
            TimeBasedRule(rounds_limit=None, doom_per_round=1.3),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-X. X is the number of Nyarlathotep enemies in play.",
                            "value": "X",
                        },
                        ("hard", "expert"): {
                            "effect": "-X. X is twice the number of Nyarlathotep enemies in play.",
                            "value": "2X",
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=2),
        ],
        ScenarioType.DARK_SIDE_OF_THE_MOON: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Lunar surface exploration
            LocationSetupRule(
                required_locations=[
                    "moon_surface",
                    "caverns_beneath",
                    "temple_of_the_moon_lizard",
                ],
            ),
            # Space/vacuum mechanics
            DynamicValueRule("lunar_environment", lambda ctx: True),
            DynamicValueRule("atmosphere_suits", lambda ctx: True),
            DynamicValueRule("low_gravity", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are not at the Moon Surface, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are not at the Moon Surface, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.POINT_OF_NO_RETURN: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Campaign choice convergence
            LocationSetupRule(
                required_locations=[
                    "the_black_expanse",
                    "ruins_of_atlantis",
                    "the_drowned_city",
                ],
            ),
            # Multiple campaign paths merging
            DynamicValueRule("campaign_convergence", lambda ctx: True),
            DynamicValueRule("atlantis_ruins", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If this test fails, place 1 doom on the current agenda.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If this test fails, place 1 doom on the current agenda.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.WHERE_THE_GODS_DWELL: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # Mount Ngranek ascent
            LocationSetupRule(
                required_locations=[
                    "base_of_ngranek",
                    "the_peaks_of_ngranek",
                    "plateau_of_leng",
                ],
            ),
            # Climbing and altitude mechanics
            DynamicValueRule("mountain_climbing", lambda ctx: True),
            DynamicValueRule("altitude_sickness", lambda ctx: True),
            DynamicValueRule("the_other_gods", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are at the highest location, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are at the highest location, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.WEAVER_OF_THE_COSMOS: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 12 + ctx["player_count"]),
            # Final boss encounter
            LocationSetupRule(
                required_locations=[
                    "the_great_web",
                    "web_woven_island",
                    "atlach_nachas_lair",
                ],
            ),
            # Web and cosmic horror mechanics
            DynamicValueRule("cosmic_web", lambda ctx: True),
            DynamicValueRule("atlach_nacha_encounter", lambda ctx: True),
            DynamicValueRule("campaign_finale", lambda ctx: True),
            # Multiple victory conditions based on campaign path
            DynamicValueRule("multiple_endings", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-4. If you fail, you are caught in the web.",
                            "value": -4,
                        },
                        ("hard", "expert"): {
                            "effect": "-6. If you fail, you are caught in the web and take 2 horror.",
                            "value": -6,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=2),
        ],
    },
)
