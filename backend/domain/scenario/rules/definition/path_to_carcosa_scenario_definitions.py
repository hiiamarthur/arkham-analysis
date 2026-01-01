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
            # Memory mechanics
            DynamicValueRule("memory_mechanics", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_UNSPEAKABLE_OATH: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Asylum return
            DynamicValueRule("asylum_return", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.A_PHANTOM_OF_TRUTH: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Theater return
            DynamicValueRule("theater_return", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_PALLID_MASK: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Masquerade mechanics
            DynamicValueRule("masquerade_mechanics", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.BLACK_STARS_RISE: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Cosmic horror
            DynamicValueRule("cosmic_horror", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.DIM_CARCOSA: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # Final scenario
            DynamicValueRule("campaign_finale", lambda ctx: True),
            DynamicValueRule("carcosa_mechanics", lambda ctx: True),
            WeaknessRule(weakness_count=1),
        ],
    },
)
