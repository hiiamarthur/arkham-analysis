"""
Path to Carcosa Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


PATH_TO_CARCOSA_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.CURTAIN_CALL: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Theater setting
            LocationSetupRule(
                required_locations=["lobby", "balcony", "backstage", "the_stage"],
            ),
            # The King in Yellow performance
            DynamicValueRule("play_performance", lambda ctx: True),
            DynamicValueRule("doubt_conviction_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-1. Add 1 doubt to your investigator.",
                            "value": -1,
                        },
                        ("hard", "expert"): {
                            "effect": "-2. Add 1 doubt to your investigator.",
                            "value": -2,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_LAST_KING: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Asylum setting
            LocationSetupRule(
                required_locations=["asylum_hallways", "garden", "kitchen", "basement"],
            ),
            # Doubt and conviction tracking
            DynamicValueRule("doubt_conviction_tracking", lambda ctx: True),
            DynamicValueRule("asylum_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you have 3+ doubt, automatically fail.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you have 2+ doubt, automatically fail.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.ECHOES_OF_THE_PAST: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            LocationSetupRule(
                required_locations=[
                    "historical_society_meeting_room",
                    "historical_society_library",
                    "historical_society_museum",
                    "historical_society_exhibit_hall",
                    "historical_society_archives",
                ],
            ),
            DynamicValueRule("memory_mechanics", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_UNSPEAKABLE_OATH: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            LocationSetupRule(
                required_locations=[
                    "cell_block",
                    "day_room",
                    "mess_hall",
                    "garden",
                    "office",
                    "bathroom",
                    "morgue",
                ],
            ),
            DynamicValueRule("asylum_return", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.A_PHANTOM_OF_TRUTH: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            LocationSetupRule(
                required_locations=[
                    "montmartre",
                    "pigalle",
                    "le_marais",
                    "montparnasse",
                    "opera_house",
                ],
                optional_locations=["the_catacombs"],
            ),
            DynamicValueRule("theater_return", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_PALLID_MASK: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            LocationSetupRule(
                required_locations=["tomb_of_shadows", "charnel_pit", "ossuary"],
                optional_locations=[
                    "vault_of_the_ancients",
                    "bone_filled_caverns",
                    "underground_river",
                ],
            ),
            DynamicValueRule("masquerade_mechanics", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.BLACK_STARS_RISE: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            LocationSetupRule(
                required_locations=[
                    "abbey_tower",
                    "abbey_church",
                    "abbots_dwelling",
                    "inner_sanctum",
                    "village_commons",
                    "the_river",
                ],
            ),
            DynamicValueRule("cosmic_horror", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.DIM_CARCOSA: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            LocationSetupRule(
                required_locations=[
                    "palace_of_the_king",
                    "the_lake_of_hali",
                    "bleak_plains",
                    "ruins_of_carcosa",
                    "depths_of_demhe",
                    "shores_of_hali",
                ],
            ),
            DynamicValueRule("campaign_finale", lambda ctx: True),
            DynamicValueRule("carcosa_mechanics", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
    },
)
