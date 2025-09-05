"""
Game difficulty levels for Arkham Horror LCG
"""

from enum import Enum


class Difficulty(Enum):
    """Difficulty levels for Arkham Horror scenarios"""
    EASY = "easy"
    STANDARD = "standard" 
    HARD = "hard"
    EXPERT = "expert"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name"""
        return self.value.title()
    
    @classmethod
    def from_string(cls, value: str) -> "Difficulty":
        """Create from string, case-insensitive"""
        for difficulty in cls:
            if difficulty.value.lower() == value.lower():
                return difficulty
        raise ValueError(f"Invalid difficulty: {value}")
    
    def __str__(self) -> str:
        return self.display_name