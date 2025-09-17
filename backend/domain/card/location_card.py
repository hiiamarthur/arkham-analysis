from dataclasses import dataclass
from .encounter_card import EncounterCard
from .card_type import CardType
from .faction import Faction
from .with_clue import WithClue
from .with_victory import WithVictory


@dataclass
class LocationCard(WithClue, WithVictory, EncounterCard):
    card_type = CardType.LOCATION
    faction = Faction.MYTHOS
    shroud: int = 0
    is_per_investigator: bool = False
