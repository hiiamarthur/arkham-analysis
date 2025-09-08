from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from .encounter_card import EncounterCard
from .card_type import CardType
from .faction import Faction


@dataclass
class ScenarioCard(EncounterCard):
    card_type = CardType.SCENARIO
    faction = Faction.MYTHOS
