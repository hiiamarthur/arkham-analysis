from dataclasses import dataclass
from typing import List, Optional

from .activation_type import ActivationType
from .card_cost_factor import CardCostFactor
from .card_type import CardType
from .player_card import PlayerCard
from .faction import Faction


@dataclass
class SkillCard(PlayerCard):
    card_type: CardType = CardType.SKILL
    cost: int = 0
    activation_type: ActivationType = ActivationType.FAST
