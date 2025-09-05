"""
Arkham Analysis API Version 1
Provides card analysis, scoring, and sync capabilities for Arkham Horror LCG
"""

from .api import api_router

# API Version Information
API_VERSION = "v1"
API_TITLE = "Arkham Analysis API"
API_DESCRIPTION = "Card analysis and scoring system for Arkham Horror: The Card Game"
API_VERSION_NUMBER = "1.0.0"

# Arkham-specific configuration
ARKHAM_CONFIG = {
    "supported_card_types": ["asset", "event", "skill", "investigator", "enemy", "treachery", "location"],
    "supported_factions": ["guardian", "seeker", "rogue", "mystic", "survivor", "neutral"],
    "max_encounter_sets": 50,
    "supported_cycles": ["core", "dunwich", "carcosa", "forgotten", "circle", "dream", "innsmouth", "edge"],
    "scoring_version": "2.0",
    "cache_version": "1.1"
}

# ArkhamDB Integration Settings
ARKHAMDB_CONFIG = {
    "api_version": "public",
    "rate_limit_per_minute": 60,
    "cache_duration_hours": 6,
    "supported_endpoints": ["cards", "taboos", "packs", "cycles"]
}

# Feature Flags for v1
FEATURES = {
    "card_scoring": True,
    "bulk_analysis": True,
    "arkhamdb_sync": True,
    "advanced_filtering": True,
    "caching": True,
    "taboo_support": True,
    "chaos_bag_simulation": False,  # Future feature
    "deck_analysis": False,         # Future feature
    "multiplayer_scenarios": False  # Future feature
}

# Version-specific constants
DEFAULT_SEARCH_LIMIT = 50
MAX_BULK_ANALYSIS_SIZE = 1000
SUPPORTED_IMAGE_FORMATS = ["jpg", "png", "webp"]

# Export what this version provides
__all__ = [
    "api_router", 
    "API_VERSION", 
    "API_TITLE", 
    "ARKHAM_CONFIG", 
    "ARKHAMDB_CONFIG", 
    "FEATURES"
]