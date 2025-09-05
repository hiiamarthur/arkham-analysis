"""
Forgotten Age Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


FORGOTTEN_AGE_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.THE_UNTAMED_WILDS: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Jungle exploration setting
            LocationSetupRule(
                required_locations=["jungle_path", "overgrown_ruins", "river_canyon"],
                optional_locations=["rope_bridge", "ancient_shrine"],
            ),
            # Jungle mechanics
            DynamicValueRule("jungle_exploration", lambda ctx: True),
            DynamicValueRule("expedition_supplies", lambda ctx: True),
            # Poison and hazard mechanics
            DynamicValueRule("poison_mechanics", lambda ctx: True),
            DynamicValueRule("jungle_hazards", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you have supplies, you may spend 1 supply to treat this token as a 0 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you have supplies, you may spend 1 supply to treat this token as a -1 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_DOOM_OF_EZTLI: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Ancient Aztec temple
            LocationSetupRule(
                required_locations=["temple_entrance", "grand_chamber", "burial_pit"],
                optional_locations=["ancient_altar", "stone_stairs"],
            ),
            # Temple exploration
            DynamicValueRule("ancient_temple", lambda ctx: True),
            DynamicValueRule("temple_exploration", lambda ctx: True),
            # Relic mechanics
            DynamicValueRule("relic_mechanics", lambda ctx: True),
            # Poison continues
            DynamicValueRule("poison_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are in the Temple, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are in the Temple, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THREADS_OF_FATE: [
            PlayerCountScalingRule("starting_clues", 4, per_player=2),
            # Special doom mechanics - no standard doom threshold
            DynamicValueRule(
                "doom_threshold", lambda ctx: 999
            ),  # Effectively no doom limit
            # Mexico City investigation
            LocationSetupRule(
                required_locations=["mexico_city", "templo_mayor", "xochimilco"],
                optional_locations=["museum", "zocalo", "train_depot"],
            ),
            # Multiple investigation tracks
            DynamicValueRule("multiple_investigations", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Time mechanics introduction
            DynamicValueRule("time_mechanics", lambda ctx: True),
            # No time pressure - investigation scenario
            TimeBasedRule(rounds_limit=None, doom_per_round=0.0),  # No automatic doom
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are investigating, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are investigating, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_BOUNDARY_BEYOND: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Dimensional rift setting
            LocationSetupRule(
                required_locations=[
                    "dimensional_gap",
                    "another_dimension",
                    "boundary_beyond",
                ],
            ),
            # Dimensional travel mechanics
            DynamicValueRule("dimensional_travel", lambda ctx: True),
            DynamicValueRule("reality_shift", lambda ctx: True),
            # Yig serpent mechanics
            DynamicValueRule("yig_mechanics", lambda ctx: True),
            # Exploration of other dimensions
            DynamicValueRule("exploration_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are in Another Dimension, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are in Another Dimension, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.HEART_OF_THE_ELDERS: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # K'n-yan underground city
            LocationSetupRule(
                required_locations=["kn_yan", "pillars_of_judgment", "the_great_abyss"],
                optional_locations=["mouth_of_kn_yan", "city_of_pnakotus"],
            ),
            # Two-part scenario mechanics
            DynamicValueRule("multi_part_scenario", lambda ctx: True),
            DynamicValueRule("underground_civilization", lambda ctx: True),
            # Elder Thing technology
            DynamicValueRule("elder_thing_technology", lambda ctx: True),
            # Alejandro Vela confrontation
            DynamicValueRule("alejandro_vela", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you control a Relic asset, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you control a Relic asset, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_CITY_OF_ARCHIVES: [
            PlayerCountScalingRule("starting_clues", 4, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Yithian city of knowledge
            LocationSetupRule(
                required_locations=[
                    "city_of_archives",
                    "great_library",
                    "yithian_halls",
                ],
            ),
            # Body swap mechanics
            DynamicValueRule("body_swap_mechanics", lambda ctx: True),
            DynamicValueRule("yithian_technology", lambda ctx: True),
            # Archive investigation
            DynamicValueRule("archive_mechanics", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Knowledge and memory themes
            DynamicValueRule("knowledge_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you have swapped bodies this scenario, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you have swapped bodies this scenario, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_DEPTHS_OF_YOTH: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Descent into underground realm
            LocationSetupRule(
                required_locations=["steps_of_yoth", "caverns_of_yoth"],
            ),
            # Descent mechanics
            DynamicValueRule("descent_mechanics", lambda ctx: True),
            DynamicValueRule("underground_realm", lambda ctx: True),
            # Exploration with depth levels
            DynamicValueRule("depth_level_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-X. X is the current depth level.",
                            "value": "X",
                        },
                        ("hard", "expert"): {
                            "effect": "-X. X is twice the current depth level.",
                            "value": "2X",
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.SHATTERED_AEONS: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 13 + ctx["player_count"]),
            # Time manipulation finale
            LocationSetupRule(
                required_locations=["nexus_of_n_kai", "temporal_nexus"],
            ),
            # Campaign finale with time mechanics
            DynamicValueRule("campaign_finale", lambda ctx: True),
            DynamicValueRule("time_manipulation", lambda ctx: True),
            DynamicValueRule("temporal_mechanics", lambda ctx: True),
            # Boss fight with Yig
            DynamicValueRule("boss_fight", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If this skill test fails, you may return an asset you control to your hand to automatically succeed instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-5. If this skill test fails, you may return an asset you control to your hand to treat this as a -1 instead.",
                            "value": -5,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
