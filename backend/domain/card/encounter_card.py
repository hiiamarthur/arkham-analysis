from abc import abstractmethod
from typing import List, Optional
from . import CardType
from . import Faction
from .base_card import BaseCard


class EncounterCard(BaseCard):
    def __init__(
        self,
        code: str,
        name: str,
        card_type: CardType,
        traits: List[str],
        faction: Faction,
        text: str,
        encounter_code: str,
        back_text: Optional[str] | None = None,
    ):
        super().__init__(
            code,
            name,
            card_type,
            traits,
            faction,
            text,
            back_text,
        )
        self.encounter_code = encounter_code

    def apply_taboo(self) -> "EncounterCard":
        return self
