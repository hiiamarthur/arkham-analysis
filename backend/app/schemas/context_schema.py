from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class PlayStyle(str, Enum):
    AGGRESSIVE = "aggressive"
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    SUPPORT = "support"
    CONTROL = "control"


class DifficultyPreference(str, Enum):
    EASY = "easy"
    STANDARD = "standard"
    HARD = "hard"
    EXPERT = "expert"


class GroupSize(str, Enum):
    SOLO = "solo"
    TWO_PLAYER = "two_player"
    THREE_PLAYER = "three_player"
    FOUR_PLAYER = "four_player"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERIENCED = "experienced"
    EXPERT = "expert"


class UserContextSchema(BaseModel):
    """User-specific context for personalized card analysis"""
    
    # Player Experience and Preferences
    experience_level: ExperienceLevel = Field(
        default=ExperienceLevel.INTERMEDIATE,
        description="Player's experience level with Arkham Horror"
    )
    play_style: PlayStyle = Field(
        default=PlayStyle.BALANCED,
        description="Preferred play style"
    )
    
    # Game Preferences
    preferred_difficulty: DifficultyPreference = Field(
        default=DifficultyPreference.STANDARD,
        description="Usually played difficulty level"
    )
    typical_group_size: GroupSize = Field(
        default=GroupSize.TWO_PLAYER,
        description="Most common group size"
    )
    
    # Investigator Preferences
    favorite_investigators: List[str] = Field(
        default=[],
        description="List of investigator codes the user prefers"
    )
    avoided_investigators: List[str] = Field(
        default=[],
        description="List of investigator codes the user avoids"
    )
    
    # Card Collection and Constraints
    owned_packs: List[str] = Field(
        default=[],
        description="List of pack codes the user owns"
    )
    taboo_adherence: bool = Field(
        default=True,
        description="Whether user follows current taboo list"
    )
    
    # Budget Constraints
    max_xp_budget: Optional[int] = Field(
        default=None,
        description="Maximum XP willing to spend on upgrades"
    )
    prefer_budget_builds: bool = Field(
        default=False,
        description="Prefer lower-cost card recommendations"
    )
    
    # Campaign Context
    current_campaign: Optional[str] = Field(
        default=None,
        description="Currently playing campaign code"
    )
    completed_campaigns: List[str] = Field(
        default=[],
        description="List of completed campaign codes"
    )
    
    # Analysis Preferences
    weight_preferences: Dict[str, float] = Field(
        default={
            "popularity": 1.0,
            "efficiency": 1.0,
            "versatility": 1.0,
            "synergy": 1.0,
            "cost_effectiveness": 1.0
        },
        description="Weights for different analysis factors (0.0-2.0)"
    )
    
    # Custom Notes
    notes: Optional[str] = Field(
        default=None,
        description="Additional user notes or preferences"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "experience_level": "intermediate",
                "play_style": "aggressive",
                "preferred_difficulty": "standard",
                "typical_group_size": "two_player",
                "favorite_investigators": ["01001", "02001"],
                "owned_packs": ["core", "dwl", "ptc"],
                "taboo_adherence": True,
                "max_xp_budget": 15,
                "current_campaign": "dwl",
                "weight_preferences": {
                    "popularity": 1.2,
                    "efficiency": 1.5,
                    "versatility": 0.8,
                    "synergy": 1.0,
                    "cost_effectiveness": 1.3
                }
            }
        }


class UserContextCreateRequest(BaseModel):
    """Request schema for creating user context"""
    user_context: UserContextSchema


class UserContextResponse(BaseModel):
    """Response schema for user context operations"""
    success: bool
    message: str
    user_context: Optional[UserContextSchema] = None