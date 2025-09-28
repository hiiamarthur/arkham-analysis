from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from enum import Enum


class DifficultyLevel(str, Enum):
    EASY = "easy"
    STANDARD = "standard"
    HARD = "hard"
    EXPERT = "expert"


class PhaseType(str, Enum):
    INVESTIGATION = "investigation"
    ENEMY = "enemy"
    UPKEEP = "upkeep"
    MYTHOS = "mythos"


class LocationStatus(str, Enum):
    UNREVEALED = "unrevealed"
    REVEALED = "revealed"
    RESIGNED = "resigned"


class InvestigatorCondition(BaseModel):
    """Current state of an investigator"""
    investigator_code: str
    current_health: int
    max_health: int
    current_sanity: int
    max_sanity: int
    current_resources: int
    current_actions: int = Field(default=3, description="Actions remaining this turn")
    doom_on_investigator: int = Field(default=0)
    horror_this_round: int = Field(default=0)
    damage_this_round: int = Field(default=0)
    is_engaged: bool = Field(default=False, description="Engaged with enemy")
    location_code: Optional[str] = Field(default=None, description="Current location")


class EnemyInPlay(BaseModel):
    """Enemy currently in play"""
    enemy_code: str
    current_health: int
    max_health: int
    doom_on_enemy: int = Field(default=0)
    location_code: Optional[str] = Field(default=None)
    engaged_with: Optional[str] = Field(default=None, description="Investigator code")
    is_exhausted: bool = Field(default=False)
    is_ready: bool = Field(default=True)


class LocationInPlay(BaseModel):
    """Location currently in play"""
    location_code: str
    status: LocationStatus
    current_clues: int
    doom_on_location: int = Field(default=0)
    investigators_here: List[str] = Field(default=[])
    enemies_here: List[str] = Field(default=[])


class TreacheryInPlay(BaseModel):
    """Treachery with lasting effects"""
    treachery_code: str
    attached_to: Optional[str] = Field(default=None, description="What it's attached to")
    doom_on_treachery: int = Field(default=0)
    rounds_remaining: Optional[int] = Field(default=None)


class GameContextSchema(BaseModel):
    """Current game state context for GPT analysis"""
    
    # Scenario Progress
    current_scenario: str = Field(description="Current scenario code")
    current_act: int = Field(default=1, description="Current Act number")
    current_agenda: int = Field(default=1, description="Current Agenda number")
    scenario_difficulty: DifficultyLevel = Field(default=DifficultyLevel.STANDARD)
    current_phase: PhaseType = Field(default=PhaseType.INVESTIGATION)
    turn_number: int = Field(default=1, description="Current turn number")
    
    # Doom and Pressure
    doom_on_agenda: int = Field(default=0, description="Current doom on agenda")
    doom_threshold: int = Field(description="Doom threshold for current agenda")
    total_doom_in_play: int = Field(default=0, description="Total doom across all sources")
    
    # Investigators State
    investigators: List[InvestigatorCondition] = Field(description="Current investigator states")
    active_investigator: str = Field(description="Code of investigator whose turn it is")
    
    # Threats in Play
    enemies_in_play: List[EnemyInPlay] = Field(default=[], description="Current enemies")
    locations_in_play: List[LocationInPlay] = Field(default=[], description="Current locations")
    treacheries_in_play: List[TreacheryInPlay] = Field(default=[], description="Lasting treacheries")
    
    # Resource State
    victory_points: int = Field(default=0, description="Victory points earned")
    experience_gained: int = Field(default=0, description="XP gained this scenario")
    
    # Environmental Factors
    chaos_tokens_remaining: Dict[str, int] = Field(
        default={}, 
        description="Chaos tokens remaining in bag"
    )
    special_rules_active: List[str] = Field(
        default=[], 
        description="Special scenario rules currently active"
    )
    
    # Analysis Context
    analysis_question: str = Field(
        description="Specific question or decision to analyze"
    )
    available_actions: List[str] = Field(
        default=[], 
        description="Actions the active investigator can take"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "current_scenario": "01104",
                "current_act": 2,
                "current_agenda": 2,
                "scenario_difficulty": "standard",
                "current_phase": "investigation",
                "turn_number": 5,
                "doom_on_agenda": 3,
                "doom_threshold": 6,
                "total_doom_in_play": 4,
                "investigators": [
                    {
                        "investigator_code": "01001",
                        "current_health": 7,
                        "max_health": 9,
                        "current_sanity": 5,
                        "max_sanity": 5,
                        "current_resources": 2,
                        "current_actions": 3,
                        "location_code": "01111"
                    }
                ],
                "active_investigator": "01001",
                "enemies_in_play": [
                    {
                        "enemy_code": "01159",
                        "current_health": 3,
                        "max_health": 3,
                        "location_code": "01111",
                        "engaged_with": "01001"
                    }
                ],
                "analysis_question": "Should I fight the enemy or try to evade it?"
            }
        }


class GameContextCreateRequest(BaseModel):
    """Request schema for creating game context"""
    game_context: GameContextSchema


class GameContextResponse(BaseModel):
    """Response schema for game context operations"""
    success: bool
    message: str
    game_context: Optional[GameContextSchema] = None