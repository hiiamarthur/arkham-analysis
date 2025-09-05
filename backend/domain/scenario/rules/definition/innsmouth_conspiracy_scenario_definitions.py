"""
Innsmouth Conspiracy Campaign Scenario Definitions
"""

from typing import Dict, List, cast
from domain import ScenarioType
from ..base_rules import *


INNSMOUTH_CONSPIRACY_SCENARIOS: Dict[ScenarioType, List[ScenarioRule]] = cast(
    Dict[ScenarioType, List[ScenarioRule]],
    {
        ScenarioType.THE_PIT_OF_DESPAIR: [
            PlayerCountScalingRule("starting_clues", 1, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 7 + ctx["player_count"]),
            # Crash survival scenario
            LocationSetupRule(
                required_locations=["crash_site", "wilderness_path", "abandoned_road"],
            ),
            # Survival mechanics
            DynamicValueRule("survival_mechanics", lambda ctx: True),
            DynamicValueRule("crash_scenario", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Flashlight mechanics
            DynamicValueRule("flashlight_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-1. If it is Agenda 2, -3 instead.",
                            "value": -1,
                        },
                        ("hard", "expert"): {
                            "effect": "-2. If it is Agenda 2, -4 instead.",
                            "value": -2,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_VANISHING_OF_ELINA_HARPER: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Missing person investigation
            LocationSetupRule(
                required_locations=[
                    "arkham_advertiser",
                    "university_library",
                    "velma_dining",
                ],
            ),
            # Investigation mechanics
            DynamicValueRule("missing_person", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            DynamicValueRule("reporter_investigation", lambda ctx: True),
            # Elina Harper search
            DynamicValueRule("elina_harper_search", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If there are no clues on your location, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If there are no clues on your location, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.IN_TOO_DEEP: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Innsmouth investigation begins
            LocationSetupRule(
                required_locations=[
                    "innsmouth_harbour",
                    "fish_street_bridge",
                    "the_house_on_water_street",
                ],
            ),
            # Innsmouth setting
            DynamicValueRule("innsmouth_setting", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            DynamicValueRule("coastal_town", lambda ctx: True),
            # Deep One mechanics introduction
            DynamicValueRule("deep_one_mechanics", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are at a Coastal location, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are at a Coastal location, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.DEVIL_REEF: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Underwater/boat mechanics
            LocationSetupRule(
                required_locations=[
                    "fishing_vessel",
                    "devil_reef_surface",
                    "lighthouse_keeper",
                ],
            ),
            # Aquatic setting
            DynamicValueRule("aquatic_mechanics", lambda ctx: True),
            DynamicValueRule("boat_mechanics", lambda ctx: True),
            DynamicValueRule("underwater_exploration", lambda ctx: True),
            # Reef exploration
            DynamicValueRule("reef_exploration", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are in the water, -5 instead.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are in the water, -7 instead.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.HORROR_IN_HIGH_GEAR: [
            PlayerCountScalingRule("starting_clues", 1, per_player=1),
            DynamicValueRule("doom_threshold", lambda ctx: 8 + ctx["player_count"]),
            # Car chase scenario
            LocationSetupRule(
                required_locations=["arkham_roads", "federal_hill", "kingsport_head"],
            ),
            # Vehicle chase mechanics
            DynamicValueRule("vehicle_chase", lambda ctx: True),
            DynamicValueRule("high_speed_pursuit", lambda ctx: True),
            # Fast-paced action
            TimeBasedRule(rounds_limit=None, doom_per_round=1.4),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are in a Vehicle, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are in a Vehicle, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.A_LIGHT_IN_THE_FOG: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 9 + ctx["player_count"]),
            # Lighthouse and fog mechanics
            LocationSetupRule(
                required_locations=[
                    "falcon_point_lighthouse",
                    "lighthouse_keeper_house",
                    "rocky_crags",
                ],
            ),
            # Fog mechanics
            DynamicValueRule("fog_mechanics", lambda ctx: True),
            DynamicValueRule("lighthouse_mechanics", lambda ctx: True),
            # Oceiros boss fight
            DynamicValueRule("boss_fight", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-2. If you are at a Coastal location, -4 instead.",
                            "value": -2,
                        },
                        ("hard", "expert"): {
                            "effect": "-3. If you are at a Coastal location, -6 instead.",
                            "value": -3,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.THE_LAIR_OF_DAGON: [
            PlayerCountScalingRule("starting_clues", 3, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 10 + ctx["player_count"]),
            # Deep One city underwater
            LocationSetupRule(
                required_locations=["dagon_temple", "sunken_grotto", "y_ha_nthlei"],
            ),
            # Underwater mechanics
            DynamicValueRule("underwater_mechanics", lambda ctx: True),
            DynamicValueRule("deep_one_city", lambda ctx: True),
            DynamicValueRule("investigation_heavy", lambda ctx: True),
            # Dagon confrontation
            DynamicValueRule("boss_fight", lambda ctx: True),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-3. If you are Flooded, you automatically fail.",
                            "value": -3,
                        },
                        ("hard", "expert"): {
                            "effect": "-4. If you are Flooded, you automatically fail.",
                            "value": -4,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
        ScenarioType.INTO_THE_MAELSTROM: [
            PlayerCountScalingRule("starting_clues", 2, per_player=2),
            DynamicValueRule("doom_threshold", lambda ctx: 12 + ctx["player_count"]),
            # Final oceanic confrontation
            LocationSetupRule(
                required_locations=["the_maelstrom", "hydra_spawn", "cyclopean_ruins"],
            ),
            # Campaign finale with Hydra
            DynamicValueRule("campaign_finale", lambda ctx: True),
            DynamicValueRule("boss_fight", lambda ctx: True),
            DynamicValueRule("hydra_mechanics", lambda ctx: True),
            # Oceanic storm
            DynamicValueRule("oceanic_storm", lambda ctx: True),
            DynamicValueRule("water_mechanics", lambda ctx: True),
            # High doom pressure
            TimeBasedRule(rounds_limit=None, doom_per_round=1.3),
            ChaosTokenModificationRule(
                {
                    "skull": {
                        ("easy", "standard"): {
                            "effect": "-4. If there are 10 or more doom tokens in play, you automatically fail.",
                            "value": -4,
                        },
                        ("hard", "expert"): {
                            "effect": "-6. If there are 8 or more doom tokens in play, you automatically fail.",
                            "value": -6,
                        },
                    }
                }
            ),
            WeaknessRule(weakness_count=1),
        ],
    },
)
