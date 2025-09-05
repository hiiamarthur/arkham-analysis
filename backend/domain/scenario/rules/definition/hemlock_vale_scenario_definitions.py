"""
Feast of Hemlock Vale Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


HEMLOCK_VALE_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.WRITTEN_IN_ROCK: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Archaeological investigation
            LocationSetupRule(
                required_locations=["dig_site", "ancient_ruins", "excavation_camp"],
            ),
            # Archaeological theme
            DynamicValueRule("archaeological_investigation", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            DynamicValueRule("ancient_writing", lambda ctx: True),
            # Rock formations and caves
            DynamicValueRule("cave_exploration", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are clues on your location, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If there are clues on your location, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.HEMLOCK_HOUSE: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Haunted house investigation
            LocationSetupRule(
                required_locations=["hemlock_house", "front_porch", "basement"],
            ),
            # Haunted house mechanics
            DynamicValueRule("haunted_house", lambda ctx: True),
            DynamicValueRule("house_investigation", lambda ctx: True),
            DynamicValueRule("spectral_mechanics", lambda ctx: True),
            # Family secrets
            DynamicValueRule("family_secrets", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are in Hemlock House, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are in Hemlock House, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_SILENT_HEALTH: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Hospital/medical setting
            LocationSetupRule(
                required_locations=[
                    "silent_health_sanitarium",
                    "patient_ward",
                    "operating_room",
                ],
            ),
            # Medical horror
            DynamicValueRule("medical_horror", lambda ctx: True),
            DynamicValueRule("sanitarium_investigation", lambda ctx: True),
            DynamicValueRule("patient_records", lambda ctx: True),
            # Silent treatment themes
            DynamicValueRule("silence_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you have fewer than 4 cards in hand, you automatically fail.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you have fewer than 5 cards in hand, you automatically fail.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_LOST_SISTER: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Search and rescue scenario
            LocationSetupRule(
                required_locations=[
                    "forest_path",
                    "abandoned_cabin",
                    "sister_location",
                ],
            ),
            # Missing person investigation
            DynamicValueRule("missing_person", lambda ctx: True),
            DynamicValueRule("forest_exploration", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Sister relationship mechanics
            DynamicValueRule("family_bond", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If The Lost Sister is not in play, -5 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If The Lost Sister is not in play, -7 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_THING_IN_THE_DEPTHS: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Underground water horror
            LocationSetupRule(
                required_locations=[
                    "underground_lake",
                    "water_treatment",
                    "deep_caverns",
                ],
            ),
            # Aquatic horror
            DynamicValueRule("aquatic_horror", lambda ctx: True),
            DynamicValueRule("underwater_mechanics", lambda ctx: True),
            DynamicValueRule("depth_exploration", lambda ctx: True),
            # The Thing mechanics
            DynamicValueRule("creature_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are at a Flooded location, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are at a Flooded location, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_TWISTED_HOLLOW: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # Twisted forest setting
            LocationSetupRule(
                required_locations=["twisted_hollow", "gnarled_trees", "hollow_center"],
            ),
            # Forest distortion mechanics
            DynamicValueRule("forest_distortion", lambda ctx: True),
            DynamicValueRule("twisted_reality", lambda ctx: True),
            DynamicValueRule("hollow_mechanics", lambda ctx: True),
            # Nature gone wrong
            DynamicValueRule("corrupted_nature", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you move during this test, -5 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you move during this test, -7 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_LONGEST_NIGHT: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 12 + ctx["player_count"]),
            # Extended night scenario
            LocationSetupRule(
                required_locations=["vale_center", "moonlit_grove", "shadow_realm"],
            ),
            # Time dilation and extended duration
            DynamicValueRule("extended_night", lambda ctx: True),
            DynamicValueRule("time_dilation", lambda ctx: True),
            DynamicValueRule("shadow_mechanics", lambda ctx: True),
            # Prolonged horror
            TimeBasedRule(
                rounds_limit=None, doom_per_round=0.8
            ),  # Slower doom accumulation
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-X. X is the current round number.",
                            "value": "X",
                        },
                        ("hard", "expert"): {
                            "effect": "-X. X is twice the current round number.",
                            "value": "2X",
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.FATE_OF_THE_VALE: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 13 + ctx["player_count"]),
            # Campaign finale
            LocationSetupRule(
                required_locations=["vale_center", "hemlock_tree", "final_chamber"],
            ),
            # Vale's ultimate fate decision
            DynamicValueRule("campaign_finale", lambda ctx: True),
            DynamicValueRule("fate_decision", lambda ctx: True),
            DynamicValueRule("vale_transformation", lambda ctx: True),
            # Multiple resolution paths
            DynamicValueRule("multiple_resolutions", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-4. If this skill test fails, place 1 doom on the current agenda.",
                            "value": -4,
                        },
                        ("hard", "expert"): {
                            "effect": "-6. If this skill test fails, place 2 doom on the current agenda.",
                            "value": -6,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
