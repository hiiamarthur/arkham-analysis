from dataclasses import dataclass
from typing import Optional


@dataclass
class CardData:
    card_id: str
    cost: Optional[int]
    action_gain: Optional[float]
    card_draw: Optional[float]
    damage: Optional[float]
    clue: Optional[float]
    horror_heal: Optional[float]
    health_heal: Optional[float]
    doom: Optional[float]
    xp: Optional[int]
    # you can extend with more properties


@dataclass
class TabooData:
    xp: Optional[int]
    text: Optional[str]


@dataclass
class ScoreResult:
    card_id: str
    strength_score: float
