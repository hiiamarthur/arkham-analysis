from abc import abstractmethod
from typing import List, Optional
from .encounter_card import EncounterCard
from . import CardType
from . import Faction
from dataclasses import dataclass


@dataclass
class EnemyCard(EncounterCard):
    card_type = CardType.ENEMY
    faction = Faction.MYTHOS
    damage: int = 0
    horror: int = 0
    fight: int = 0
    evade: int = 0
    health: int = 0
