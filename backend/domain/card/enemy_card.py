from abc import abstractmethod
from typing import List, Optional
from .encounter_card import EncounterCard
from .card_type import CardType
from .faction import Faction
from dataclasses import dataclass
from .with_victory import WithVictory


@dataclass
class EnemyCard(WithVictory, EncounterCard):
    card_type: CardType = CardType.ENEMY
    faction = Faction.MYTHOS
    damage: int = 0
    horror: int = 0
    fight: int = 0
    evade: int = 0
    health: int = 0
    health_per_investigator: bool = False

    @property
    def is_X_fight(self) -> bool:
        return self.fight == -2

    @property
    def is_X_evade(self) -> bool:
        return self.evade == -2

    @property
    def is_X_health(self) -> bool:
        return self.health == -2

    @property
    def fightable(self) -> bool:
        return self.fight != 0

    @property
    def evadeable(self) -> bool:
        return self.evade != 0

    @property
    def defeatable(self) -> bool:
        return self.health != 0
