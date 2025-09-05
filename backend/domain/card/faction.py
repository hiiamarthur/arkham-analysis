from enum import Enum
from typing import List


class Faction(Enum):
    """Player factions in Arkham Horror LCG"""

    GUARDIAN = "guardian"
    SEEKER = "seeker"
    ROGUE = "rogue"
    MYSTIC = "mystic"
    SURVIVOR = "survivor"
    NEUTRAL = "neutral"
    MYTHOS = "mythos"
    MULTICLASS = "multiclass"
    NONE = "none"

    @property
    def display_name(self) -> str:
        """Human-readable faction name"""
        return self.value.title()

    @property
    def color(self) -> str:
        """Faction color (for UI purposes)"""
        color_mapping = {
            "guardian": "#2E86C1",  # Blue
            "seeker": "#F39C12",  # Orange
            "rogue": "#27AE60",  # Green
            "mystic": "#8E44AD",  # Purple
            "survivor": "#E74C3C",  # Red
            "neutral": "#5D6D7E",  # Gray
            "multiclass": "#F1C40F",  # Yellow
            "mythos": "#000000",  # Black
        }
        return color_mapping.get(self.value, "#000000")

    @property
    def is_investigator_faction(self) -> bool:
        """Check if this is a faction investigators can belong to"""
        return self != Faction.NEUTRAL

    @classmethod
    def investigator_factions(cls) -> List["Faction"]:
        """Get factions that investigators can belong to"""
        return [faction for faction in cls if faction.is_investigator_faction]

    @classmethod
    def from_code(cls, code: str | None) -> "Faction":
        """Get faction from code, returns None if not found"""
        try:
            return cls(code)
        except ValueError:
            return Faction.NONE

    def __str__(self) -> str:
        return self.display_name
