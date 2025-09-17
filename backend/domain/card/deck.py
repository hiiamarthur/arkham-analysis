from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Deck:
    name: str
    date_creation: str
    date_update: str
    investigator_code: str
    investigator_name: str
    slots: Dict[str, int]
    sideSlots: Dict[str, int] | List[Any]
    ignoreDeckLimitSlots: Optional[Dict[str, int]]
    xp_spent: Optional[int]
    xp_adjustment: Optional[int]
    exile_string: Optional[str]
    taboo_id: Optional[int]
    meta: str
    tags: str
    previous_deck: Optional[int]
    next_deck: Optional[int]

    @classmethod
    def from_dict(cls, data: dict) -> "Deck":
        return cls(**data)
