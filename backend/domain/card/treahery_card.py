from abc import abstractmethod
from typing import List, Optional
from .encounter_card import EncounterCard
from . import CardType
from . import Faction
from dataclasses import dataclass


@dataclass
class TreacheryCard(EncounterCard):
    card_type = CardType.TREACHERY
    faction = Faction.MYTHOS
