from dataclasses import dataclass
from typing import List, Optional

from . import ActivationType, CardCostFactor, CardType
from .player_card import PlayerCard
from . import Faction


@dataclass
class SkillCard(PlayerCard):
    card_type: CardType = CardType.SKILL
    cost: int = 0
    activation_type: ActivationType = ActivationType.FAST
