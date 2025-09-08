from dataclasses import dataclass
from typing import List, Optional
from . import ActivationType, CardType
from .player_card import PlayerCard
from .faction import Faction


@dataclass
class EventCard(PlayerCard):
    card_type: CardType = CardType.EVENT
    activation_type: ActivationType = ActivationType.PLAY
