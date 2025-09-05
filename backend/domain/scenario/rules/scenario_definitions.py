"""
Main Scenario Rule Registry - Imports from campaign-specific files
"""

from typing import Dict, List
from domain import ScenarioType
from .base_rules import ScenarioRule

# Import campaign-specific scenario definitions
from .definition import (
    NIGHT_OF_THE_ZEALOT_SCENARIOS,
    DUNWICH_LEGACY_SCENARIOS,
    PATH_TO_CARCOSA_SCENARIOS,
    FORGOTTEN_AGE_SCENARIOS,
    CIRCLE_UNDONE_SCENARIOS,
    DREAM_EATERS_SCENARIOS,
    INNSMOUTH_CONSPIRACY_SCENARIOS,
    EDGE_OF_THE_EARTH_SCENARIOS,
    SCARLET_KEYS_SCENARIOS,
    HEMLOCK_VALE_SCENARIOS,
    DROWNED_CITY_SCENARIOS,
)


# Import template functions
from .scenario_templates import (
    create_standard_scenario_template,
    create_investigation_heavy_template,
    create_combat_heavy_template,
)


def get_scenario_rules(scenario_type: ScenarioType) -> List[ScenarioRule]:
    """Get rules for any scenario with minimal hardcoding"""
    return SCENARIO_RULES_REGISTRY.get(scenario_type, [])


# Combined scenario rules registry
SCENARIO_RULES_REGISTRY: Dict[ScenarioType, List[ScenarioRule]] = {
    **NIGHT_OF_THE_ZEALOT_SCENARIOS,
    **DUNWICH_LEGACY_SCENARIOS,
    **PATH_TO_CARCOSA_SCENARIOS,
    **FORGOTTEN_AGE_SCENARIOS,
    **CIRCLE_UNDONE_SCENARIOS,
    **DREAM_EATERS_SCENARIOS,
    **INNSMOUTH_CONSPIRACY_SCENARIOS,
    **EDGE_OF_THE_EARTH_SCENARIOS,
    **SCARLET_KEYS_SCENARIOS,
    **HEMLOCK_VALE_SCENARIOS,
    **DROWNED_CITY_SCENARIOS,
}
