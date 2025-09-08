"""
Scenario Template Functions for Common Patterns
"""

from typing import Dict, List, cast
from .base_rules import *


def create_standard_scenario_template(
    base_clues: int = 2,
    base_doom: int = 8,
    locations: List[str] | None = None,
    special_mechanics: Dict[str, bool] | None = None,
    chaos_modifications: Dict[str, Dict] | None = None,
) -> List[ScenarioRule]:
    """Template for standard scenario setup"""
    rules = [
        PlayerCountScalingRule("starting_clues", base_clues, per_player=1),
        DynamicValueRule("doom_threshold", lambda ctx: base_doom + ctx["player_count"]),
        WeaknessRule(weakness_count=1),
    ]

    if locations:
        rules.append(LocationSetupRule(required_locations=locations))

    if special_mechanics:
        for mechanic, enabled in special_mechanics.items():
            if enabled:
                rules.append(DynamicValueRule(mechanic, lambda ctx: True))

    if chaos_modifications:
        rules.append(ChaosTokenModificationRule(chaos_modifications))

    return rules


def create_investigation_heavy_template(**kwargs) -> List[ScenarioRule]:
    """Template for investigation-focused scenarios"""
    return create_standard_scenario_template(
        base_clues=kwargs.get("base_clues", 4),
        base_doom=kwargs.get("base_doom", 10),
        special_mechanics={"investigation_heavy": True},
        **kwargs
    )


def create_combat_heavy_template(**kwargs) -> List[ScenarioRule]:
    """Template for combat-focused scenarios"""
    return create_standard_scenario_template(
        base_clues=kwargs.get("base_clues", 2),
        base_doom=kwargs.get("base_doom", 8),
        special_mechanics={
            "combat_heavy": True,
            "boss_fight": kwargs.get("boss_fight", False),
        },
        **kwargs
    )
