"""
Scarlet Keys Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


SCARLET_KEYS_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.RIDDLE_AND_RAIN: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # London setting with investigation
            LocationSetupRule(
                required_locations=[
                    "london_streets",
                    "red_coterie_hideout",
                    "thames_embankment",
                ],
            ),
            # Red Coterie introduction
            DynamicValueRule("red_coterie_mechanics", lambda ctx: True),
            DynamicValueRule("london_setting", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Riddle mechanics
            DynamicValueRule("riddle_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are at a location with no investigators, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are at a location with no investigators, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.DANCING_MAD: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Parisian nightclub
            LocationSetupRule(
                required_locations=["le_marais", "nightclub_floor", "backstage_area"],
            ),
            # Dancing and performance mechanics
            DynamicValueRule("dance_mechanics", lambda ctx: True),
            DynamicValueRule("performance_mechanics", lambda ctx: True),
            DynamicValueRule("paris_setting", lambda ctx: True),
            # Madness through dancing
            DynamicValueRule("induced_madness", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you have performed this round, you automatically fail.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you have performed this round, you automatically fail.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.ON_THIN_ICE: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Antarctic research station
            LocationSetupRule(
                required_locations=[
                    "research_station",
                    "ice_shelf",
                    "communications_tower",
                ],
            ),
            # Ice and cold mechanics
            DynamicValueRule("ice_mechanics", lambda ctx: True),
            DynamicValueRule("antarctic_research", lambda ctx: True),
            DynamicValueRule("cold_exposure", lambda ctx: True),
            # Research station isolation
            DynamicValueRule("isolation_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are at an Ice location, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are at an Ice location, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.DEAD_HEAT: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Sahara desert expedition
            LocationSetupRule(
                required_locations=[
                    "sahara_desert",
                    "archaeological_dig",
                    "bedouin_camp",
                ],
            ),
            # Heat and desert mechanics
            DynamicValueRule("heat_mechanics", lambda ctx: True),
            DynamicValueRule("desert_exploration", lambda ctx: True),
            DynamicValueRule("archaeological_site", lambda ctx: True),
            # Extreme heat exposure
            DynamicValueRule("heat_exposure", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If it is Round 4+, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If it is Round 3+, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.SANGUINE_SHADOWS: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Venice setting with vampires
            LocationSetupRule(
                required_locations=[
                    "venetian_canals",
                    "palazzo_rosso",
                    "bridge_of_sighs",
                ],
            ),
            # Vampire mechanics
            DynamicValueRule("vampire_mechanics", lambda ctx: True),
            DynamicValueRule("venice_setting", lambda ctx: True),
            DynamicValueRule("blood_mechanics", lambda ctx: True),
            # Sanguine shadows
            DynamicValueRule("shadow_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you have damage or horror, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you have damage or horror, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.DEALING_IN_THE_DARK: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Underground marketplace
            LocationSetupRule(
                required_locations=[
                    "black_market",
                    "underground_tunnel",
                    "smugglers_den",
                ],
            ),
            # Dealing and trading mechanics
            DynamicValueRule("dealing_mechanics", lambda ctx: True),
            DynamicValueRule("underground_marketplace", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Criminal underworld
            DynamicValueRule("criminal_underworld", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you have fewer than 3 resources, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you have fewer than 3 resources, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.DOGS_OF_WAR: [
            PlayerCountScalingRule("starting_clues", 2, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # War-torn battlefield
            LocationSetupRule(
                required_locations=["battlefield", "trenches", "command_post"],
            ),
            # War and combat mechanics
            DynamicValueRule("war_mechanics", lambda ctx: True),
            DynamicValueRule("combat_heavy", lambda ctx: True),
            DynamicValueRule("battlefield_setting", lambda ctx: True),
            # Chaos of war
            DynamicValueRule("chaos_of_war", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If there are enemies at your location, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If there are enemies at your location, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.SHADES_OF_SUFFERING: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Psychological horror scenario
            LocationSetupRule(
                required_locations=["sanitarium", "therapy_rooms", "isolation_ward"],
            ),
            # Mental health and suffering themes
            DynamicValueRule("psychological_horror", lambda ctx: True),
            DynamicValueRule("mental_health_mechanics", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Suffering and trauma
            DynamicValueRule("trauma_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you have horror tokens, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you have horror tokens, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.WITHOUT_A_TRACE: [
            PlayerCountScalingRule("starting_clues", 4, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 11 + ctx["player_count"]),
            # Mystery investigation
            LocationSetupRule(
                required_locations=[
                    "crime_scene",
                    "detective_office",
                    "missing_persons_bureau",
                ],
            ),
            # Investigation and mystery
            DynamicValueRule("mystery_investigation", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            DynamicValueRule("missing_persons", lambda ctx: True),
            # Detective work
            DynamicValueRule("detective_work", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are no clues on locations, -5 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If there are fewer than 2 clues on locations, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.CONGRESS_OF_THE_KEYS: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 13 + ctx["player_count"]),
            # Campaign finale
            LocationSetupRule(
                required_locations=["congress_hall", "key_chamber", "scarlet_nexus"],
            ),
            # Campaign finale with Red Coterie
            DynamicValueRule("campaign_finale", lambda ctx: True),
            DynamicValueRule("boss_fight", lambda ctx: True),
            DynamicValueRule("red_coterie_finale", lambda ctx: True),
            # Congress of the Keys
            DynamicValueRule("congress_mechanics", lambda ctx: True),
            DynamicValueRule("key_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-4. If there are fewer than 2 investigators at your location, you automatically fail.",
                            "value": -4,
                        },
                        ("hard", "expert"): {
                            "effect": "-6. If there are fewer than 3 investigators at your location, you automatically fail.",
                            "value": -6,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
