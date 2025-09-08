from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from .card_type import CardType
from .faction import Faction
from .base_card import BaseCard


@dataclass
class EncounterCard(BaseCard):
    encounter_code: str = ""

    def apply_taboo(self) -> "EncounterCard":
        return self
