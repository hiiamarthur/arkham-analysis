from dataclasses import dataclass
from typing import List, Optional
from .activation_type import ActivationType
from .card_type import CardType
from .player_card import PlayerCard
from .faction import Faction


@dataclass
class EventCard(PlayerCard):
    card_type: CardType = CardType.EVENT
    activation_type: ActivationType = ActivationType.PLAY

    # def __post_init__(self):
    #     super().__post_init__()
    #     # Override card_type for event cards
    #     if self.card_type != CardType.EVENT:
    #         object.__setattr__(self, 'card_type', CardType.EVENT)
