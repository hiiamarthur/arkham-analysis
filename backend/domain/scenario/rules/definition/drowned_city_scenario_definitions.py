"""
Drowned City Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


DROWNED_CITY_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.ONE_LAST_JOB: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Heist scenario opening
            LocationSetupRule(
                required_locations=["bank_exterior", "vault_entrance", "getaway_route"],
            ),
            # Heist mechanics
            DynamicValueRule("heist_mechanics", lambda ctx: True),
            DynamicValueRule("stealth_mechanics", lambda ctx: True),
            DynamicValueRule("time_pressure", lambda ctx: True),
            # Criminal enterprise
            DynamicValueRule("criminal_enterprise", lambda ctx: True),
            TimeBasedRule(rounds_limit=12, doom_per_round=1.2),  # Time pressure
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you fail, gain 1 heat token.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you fail, gain 2 heat tokens.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_WESTERN_WALL: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Flooded city exploration
            LocationSetupRule(
                required_locations=[
                    "western_wall",
                    "flooded_street",
                    "emergency_shelter",
                ],
            ),
            # Flood mechanics
            DynamicValueRule("flood_mechanics", lambda ctx: True),
            DynamicValueRule("water_navigation", lambda ctx: True),
            DynamicValueRule("structural_damage", lambda ctx: True),
            # Urban disaster
            DynamicValueRule("urban_disaster", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are at a Flooded location, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are at a Flooded location, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_DROWNED_QUARTER: [
            PlayerCountScalingRule("starting_clues", 4, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Underwater city district
            LocationSetupRule(
                required_locations=[
                    "drowned_quarter",
                    "submerged_buildings",
                    "air_pocket",
                ],
            ),
            # Underwater exploration
            DynamicValueRule("underwater_exploration", lambda ctx: True),
            DynamicValueRule("breathing_mechanics", lambda ctx: True),
            DynamicValueRule("aquatic_investigation", lambda ctx: True),
            # Drowned city atmosphere
            DynamicValueRule("drowned_atmosphere", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you have no air supply, you automatically fail.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you have no air supply, you automatically fail.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_APIARY: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Insect/hive mechanics
            LocationSetupRule(
                required_locations=["the_apiary", "queen_chamber", "honeycomb_maze"],
            ),
            # Bee/hive mechanics
            DynamicValueRule("hive_mechanics", lambda ctx: True),
            DynamicValueRule("swarm_encounters", lambda ctx: True),
            DynamicValueRule("queen_mechanics", lambda ctx: True),
            # Apiary investigation
            DynamicValueRule("apiary_investigation", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are Swarm enemies in play, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If there are Swarm enemies in play, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_GRAND_VAULT: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # Bank vault heist
            LocationSetupRule(
                required_locations=["grand_vault", "security_systems", "treasure_room"],
            ),
            # Vault mechanics
            DynamicValueRule("vault_mechanics", lambda ctx: True),
            DynamicValueRule("security_systems", lambda ctx: True),
            DynamicValueRule("treasure_hunting", lambda ctx: True),
            # High-stakes heist
            DynamicValueRule("high_stakes_heist", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If security is active, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If security is active, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.COURT_OF_THE_ANCIENTS: [
            PlayerCountScalingRule("starting_clues", 4, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 12 + ctx["player_count"]),
            # Ancient court/tribunal
            LocationSetupRule(
                required_locations=["ancient_court", "judgment_hall", "elder_chambers"],
            ),
            # Ancient powers and judgment
            DynamicValueRule("ancient_powers", lambda ctx: True),
            DynamicValueRule("tribunal_mechanics", lambda ctx: True),
            DynamicValueRule("judgment_mechanics", lambda ctx: True),
            # Court proceedings
            DynamicValueRule("court_proceedings", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-4. If you are being judged, you automatically fail.",
                            "value": -4,
                        },
                        ("hard", "expert"): {
                            "effect": "-6. If you are being judged, you automatically fail.",
                            "value": -6,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.OBSIDIAN_CANYONS: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Volcanic/canyon setting
            LocationSetupRule(
                required_locations=["obsidian_canyon", "lava_flows", "crystal_caves"],
            ),
            # Volcanic/geological mechanics
            DynamicValueRule("volcanic_mechanics", lambda ctx: True),
            DynamicValueRule("canyon_exploration", lambda ctx: True),
            DynamicValueRule("heat_mechanics", lambda ctx: True),
            # Obsidian and crystal themes
            DynamicValueRule("crystal_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are at a Volcanic location, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are at a Volcanic location, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.SEPULCHRE_OF_THE_SLEEPERS: [
            PlayerCountScalingRule("starting_clues", 4, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 13 + ctx["player_count"]),
            # Ancient tomb/burial site
            LocationSetupRule(
                required_locations=[
                    "sepulchre_entrance",
                    "burial_chambers",
                    "sleeper_sanctum",
                ],
            ),
            # Tomb exploration and awakening
            DynamicValueRule("tomb_exploration", lambda ctx: True),
            DynamicValueRule("sleeper_mechanics", lambda ctx: True),
            DynamicValueRule("awakening_mechanics", lambda ctx: True),
            # Ancient burial rites
            DynamicValueRule("burial_rites", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-4. If there are awakened Sleepers, -6 instead.",
                            "value": -4,
                        },
                        ("hard", "expert"): {
                            "effect": "-5. If there are awakened Sleepers, -8 instead.",
                            "value": -5,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_DOOM_OF_ARKHAM_PT_I: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 14 + ctx["player_count"]),
            # Campaign finale Part 1
            LocationSetupRule(
                required_locations=[
                    "arkham_center",
                    "miskatonic_university",
                    "rivertown",
                ],
            ),
            # Arkham under threat
            DynamicValueRule("arkham_under_siege", lambda ctx: True),
            DynamicValueRule("city_wide_crisis", lambda ctx: True),
            DynamicValueRule("multi_part_finale", lambda ctx: True),
            # Campaign finale mechanics
            DynamicValueRule("campaign_finale", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-5. If this skill test fails, place 1 doom on the current agenda.",
                            "value": -5,
                        },
                        ("hard", "expert"): {
                            "effect": "-7. If this skill test fails, place 2 doom on the current agenda.",
                            "value": -7,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_DOOM_OF_ARKHAM_PT_II: [
            PlayerCountScalingRule("starting_clues", 4, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 16 + ctx["player_count"]),
            # Campaign finale Part 2
            LocationSetupRule(
                required_locations=[
                    "arkham_ruins",
                    "final_confrontation",
                    "nexus_of_power",
                ],
            ),
            # Final battle for Arkham
            DynamicValueRule("final_battle", lambda ctx: True),
            DynamicValueRule("boss_fight", lambda ctx: True),
            DynamicValueRule("arkham_finale", lambda ctx: True),
            # Ultimate campaign finale
            DynamicValueRule("ultimate_finale", lambda ctx: True),
            TimeBasedRule(rounds_limit=None, doom_per_round=1.5),  # High pressure
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-6. If this skill test fails, place 2 doom on the current agenda.",
                            "value": -6,
                        },
                        ("hard", "expert"): {
                            "effect": "-8. If this skill test fails, place 3 doom on the current agenda.",
                            "value": -8,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
