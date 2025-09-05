from abc import abstractmethod
from typing import List, Optional
from .encounter_card import EncounterCard
from . import CardType
from . import Faction


class EnemyCard(EncounterCard):
    def __init__(
        self,
        code: str,
        name: str,
        traits: List[str],
        text: str,
        encounter_code: str,
        back_text: Optional[str],
        damage: int,
        horror: int,
        fight: int,
        evade: int,
        health: int,
    ):
        super().__init__(
            code,
            name,
            CardType.ENEMY,
            traits,
            Faction.MYTHOS,
            text,
            encounter_code,
            back_text,
        )
        self.damage = damage
        self.horror = horror
        self.fight = fight
        self.evade = evade
        self.health = health
