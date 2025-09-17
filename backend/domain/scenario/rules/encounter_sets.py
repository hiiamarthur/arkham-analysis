"""
Encounter Set Registry - Complete mapping of encounter sets for all scenarios
"""

from calendar import TUESDAY
from re import I
from typing import Any, Dict, List, Set
import sys
import os

backend_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."
)
if backend_path not in sys.path:
    sys.path.append(backend_path)

from .encounter_set import (
    CORE_ENCOUNTER_SET,
    DUNWICH_ENCOUNTER_SET,
    CARCOSA_ENCOUNTER_SET,
    FORGOTTEN_AGE_ENCOUNTER_SET,
    CIRCLE_UNDONE_ENCOUNTER_SET,
    DREAM_EATERS_ENCOUNTER_SET,
    INNOMOUNT_ENCOUNTER_SET,
    EDGE_OF_THE_EARTH_ENCOUNTER_SET,
    SCARLET_KEYS_ENCOUNTER_SET,
    HEMLOCK_ENCOUNTER_SET,
    DROWNED_CITY_ENCOUNTER_SET,
)
from domain import ScenarioType

# Complete encounter set registry for Arkham Horror LCG
ENCOUNTER_SET_REGISTRY = {
    **CORE_ENCOUNTER_SET,
    **DUNWICH_ENCOUNTER_SET,
    **CARCOSA_ENCOUNTER_SET,
    **FORGOTTEN_AGE_ENCOUNTER_SET,
    **CIRCLE_UNDONE_ENCOUNTER_SET,
    **DREAM_EATERS_ENCOUNTER_SET,
    **INNOMOUNT_ENCOUNTER_SET,
    **EDGE_OF_THE_EARTH_ENCOUNTER_SET,
    **SCARLET_KEYS_ENCOUNTER_SET,
    **HEMLOCK_ENCOUNTER_SET,
    **DROWNED_CITY_ENCOUNTER_SET,
}


def get_encounter_set(encounter_code: str) -> Dict[str, Any]:
    """Get encounter set by code"""
    return ENCOUNTER_SET_REGISTRY.get(encounter_code, {})


def get_encounter_set_by_name(name: str) -> Dict[str, Any]:
    """Get encounter set by name"""
    print("encounter_set is", name)
    for encounter_code, encounter_set in ENCOUNTER_SET_REGISTRY.items():
        print("encounter_set is", encounter_set, name)
        if encounter_set.get("name", "").lower() == name.lower():
            # Return the encounter set data with the code included
            return {"code": encounter_code, **encounter_set}
    return {}


def get_encounter_sets_for_scenario(
    scenario_type: ScenarioType,
) -> List[str]:
    """Get all encounter sets for a scenario"""
    encounter_sets = []

    for set_code, set_info in ENCOUNTER_SET_REGISTRY.items():
        if scenario_type in set_info["scenarios"]:
            encounter_sets.append(set_code)

    return encounter_sets


def get_random_encounter_groups(scenario_type: ScenarioType) -> Dict[str, List[str]]:
    """Get random encounter set groups for scenarios that need them"""
    random_groups = {
        ScenarioType.THE_DEVOURER_BELOW: {
            "agents_group": [
                "agents_of_yog_sothoth",
                "agents_of_shub_niggurath",
                "agents_of_cthulhu",
                "agents_of_hastur",
            ]
        },
        # Add more scenarios with random groups
    }

    return random_groups.get(scenario_type, {})


# def validate_encounter_set_setup(
#     scenario_type: ScenarioType, selected_sets: List[str]
# ) -> List[str]:
#     """Validate that encounter set selection is valid for scenario"""
#     errors = []
#     encounter_info = get_encounter_sets_for_scenario(scenario_type)
#     random_groups = get_random_encounter_groups(scenario_type)

#     # Check required sets are present
#     for required_set in encounter_info["required"]:
#         if required_set not in selected_sets:
#             errors.append(f"Missing required encounter set: {required_set}")

#     # Check random selection rules
#     for group_name, group_sets in random_groups.items():
#         selected_from_group = [s for s in selected_sets if s in group_sets]
#         if len(selected_from_group) != 1:
#             errors.append(
#                 f"Must select exactly 1 set from {group_name}, got {len(selected_from_group)}"
#             )

#     return errors


# def get_encounter_set_stats(scenario_type: ScenarioType) -> Dict[str, Any]:
#     """Get statistical information about encounter sets for scenario"""
#     encounter_info = get_encounter_sets_for_scenario(scenario_type)
#     random_groups = get_random_encounter_groups(scenario_type)

#     return {
#         "total_required_sets": len(encounter_info["required"]),
#         "total_random_options": len(encounter_info["random_selection"]),
#         "random_groups": len(random_groups),
#         "max_possible_combinations": (
#             max(1, len(encounter_info["random_selection"]))
#             if encounter_info["random_selection"]
#             else 1
#         ),
#         "encounter_variety_score": len(encounter_info["required"])
#         + len(encounter_info["random_selection"]) * 0.5,
#     }
