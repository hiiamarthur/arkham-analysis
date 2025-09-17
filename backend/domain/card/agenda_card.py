from dataclasses import dataclass
from .encounter_card import EncounterCard
from .card_type import CardType
from .faction import Faction


@dataclass
class AgendaCard(EncounterCard):
    card_type = CardType.AGENDA
    faction = Faction.MYTHOS
    doom = 0
    stage = 0
