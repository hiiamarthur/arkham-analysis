from abc import abstractmethod
from typing import List, Optional
from .encounter_card import EncounterCard
from . import CardType
from . import Faction


class TreacheryCard(EncounterCard):
    def __init__(
        self,
        code: str,
        name: str,
        traits: List[str],
        text: str,
        encounter_code: str,
        back_text: Optional[str],
    ):
        super().__init__(
            code,
            name,
            CardType.TREACHERY,
            traits,
            Faction.MYTHOS,
            text,
            encounter_code,
            back_text,
        )
