from .faction import Faction
from .card_type import CardType
from dataclasses import dataclass
from .encounter_card import EncounterCard


@dataclass
class ActCard(EncounterCard):
    card_type = CardType.ACT
    faction = Faction.MYTHOS
    stage = 0
