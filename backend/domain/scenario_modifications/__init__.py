"""
Unified scenario chaos token modifications, organized by campaign.
Each campaign module uses plain string keys (snake_case scenario names)
to avoid circular imports with scenarios.py.
"""
from typing import Dict, Tuple, Any

from .night_of_the_zealot import NIGHT_OF_THE_ZEALOT_MODIFICATIONS
from .dunwich_legacy import DUNWICH_LEGACY_MODIFICATIONS
from .path_to_carcosa import PATH_TO_CARCOSA_MODIFICATIONS
from .forgotten_age import FORGOTTEN_AGE_MODIFICATIONS
from .circle_undone import CIRCLE_UNDONE_MODIFICATIONS
from .dream_eaters import DREAM_EATERS_MODIFICATIONS
from .innsmouth_conspiracy import INNSMOUTH_CONSPIRACY_MODIFICATIONS

# Merged dict: scenario_key (str) -> token_type -> difficulty_tuple -> effect data
ALL_SCENARIO_MODIFICATIONS: Dict[str, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]] = {
    **NIGHT_OF_THE_ZEALOT_MODIFICATIONS,
    **DUNWICH_LEGACY_MODIFICATIONS,
    **PATH_TO_CARCOSA_MODIFICATIONS,
    **FORGOTTEN_AGE_MODIFICATIONS,
    **CIRCLE_UNDONE_MODIFICATIONS,
    **DREAM_EATERS_MODIFICATIONS,
    **INNSMOUTH_CONSPIRACY_MODIFICATIONS,
}

__all__ = ["ALL_SCENARIO_MODIFICATIONS"]
