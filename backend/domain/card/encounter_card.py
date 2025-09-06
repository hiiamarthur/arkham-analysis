from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from . import CardType
from . import Faction
from .base_card import BaseCard


@dataclass
class EncounterCard(BaseCard):
    encounter_code: str = ""

    def apply_taboo(self) -> "EncounterCard":
        return self
