"""
General game type definitions for Arkham Horror LCG
"""

from enum import Enum
from typing import Dict, List, Set


# EncounterSet is now handled by the database (EncounterSetModel)
# This provides more flexibility for dynamic encounter sets from ArkhamDB


# Skill icons
class SkillIcon(Enum):
    """Skill icons on cards"""

    WILLPOWER = "willpower"
    INTELLECT = "intellect"
    COMBAT = "combat"
    AGILITY = "agility"
    WILD = "wild"

    @property
    def display_name(self) -> str:
        return self.value.title()

    @property
    def symbol(self) -> str:
        """Unicode symbol for skill icon"""
        symbols = {
            "willpower": "♦",
            "intellect": "●",
            "combat": "⚔",
            "agility": "⚡",
            "wild": "★",
        }
        return symbols.get(self.value, "?")

    def __str__(self) -> str:
        return self.symbol


# Slot restrictions
class Slot(Enum):
    """Equipment slots for assets"""

    HAND = "hand"
    BODY = "body"
    ACCESSORY = "accessory"
    ALLY = "ally"
    ARCANE = "arcane"
    TAROT = "tarot"

    @property
    def display_name(self) -> str:
        return self.value.title()

    def __str__(self) -> str:
        return self.display_name


# Card traits - common ones
COMMON_TRAITS: Dict[str, Set[str]] = {
    "investigator": {
        "Agency",
        "Drifter",
        "Miskatonic",
        "Scholar",
        "Veteran",
        "Wayfarer",
    },
    "asset": {"Item", "Weapon", "Spell", "Ally", "Talent", "Condition", "Ritual"},
    "enemy": {"Monster", "Humanoid", "Cultist", "Ancient One", "Elite"},
    "location": {"Arkham", "Miskatonic", "Downtown", "Easttown", "Northside"},
}
