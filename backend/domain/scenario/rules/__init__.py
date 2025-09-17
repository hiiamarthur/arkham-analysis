"""
Scenario Rules - Declarative rule system for scenario mechanics
"""

from .base_rules import (
    ScenarioRule,
    RandomEncounterSetRule,
    ConditionalLocationRule,
    DynamicValueRule,
    PlayerCountScalingRule,
    ChaosTokenModificationRule,
    TimeBasedRule,
    LocationSetupRule,
    InvestigatorDependentRule,
    ProgressiveRule,
)

from .scenario_definitions import get_scenario_rules
from .encounter_sets import (
    ENCOUNTER_SET_REGISTRY,
    get_encounter_sets_for_scenario,
    get_encounter_set,
    get_encounter_set_by_name,
)
from .scenario_templates import (
    create_standard_scenario_template,
    create_investigation_heavy_template,
    create_combat_heavy_template,
)

__all__ = [
    # Base Rules
    "ScenarioRule",
    "RandomEncounterSetRule",
    "ConditionalLocationRule",
    "DynamicValueRule",
    "PlayerCountScalingRule",
    "ChaosTokenModificationRule",
    "TimeBasedRule",
    "LocationSetupRule",
    "InvestigatorDependentRule",
    "ProgressiveRule",
    # Registry
    "get_scenario_rules",
    "ENCOUNTER_SET_REGISTRY",
    "get_encounter_sets_for_scenario",
    "get_encounter_set",
    "get_encounter_set_by_name",
    # Templates
    "create_standard_scenario_template",
    "create_investigation_heavy_template",
    "create_combat_heavy_template",
]
