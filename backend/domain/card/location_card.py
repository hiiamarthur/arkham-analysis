from dataclasses import dataclass
from .encounter_card import EncounterCard
from .card_type import CardType
from .faction import Faction


@dataclass
class LocationCard(EncounterCard):
    card_type = CardType.LOCATION
    faction = Faction.MYTHOS
    shroud: int = 0
    clues: int = 0
    is_per_investigator: bool = False
