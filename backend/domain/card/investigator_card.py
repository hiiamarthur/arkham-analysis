from dataclasses import dataclass, field
from typing import Any, Dict, List

from .faction import Faction
from .card_type import CardType
from .base_card import BaseCard
from .with_health_sanity import WithHealthSanity


@dataclass
class InvestigatorCard(BaseCard, WithHealthSanity):
    deck_limit: Dict[str, Any] = field(default_factory=dict)
    card_type: CardType = CardType.INVESTIGATOR
    play_action_cost: int = 0
    is_unique: bool = True
    is_permanent: bool = True

    # def __init__(
    #     self,
    #     code: str,
    #     name: str,
    #     traits: List[str],
    #     text: str,
    #     skill_willpower: int,
    #     skill_intellect: int,
    #     skill_combat: int,
    #     skill_agility: int,
    #     faction: Faction,
    #     health: int,
    #     sanity: int,
    # ):
    #     super().__init__(
    #         code,
    #         name,
    #         CardType.INVESTIGATOR,
    #         traits,
    #         faction,
    #         text,
    #         "",
    #     )
    #     self.skill_willpower = skill_willpower
    #     self.skill_intellect = skill_intellect
    #     self.skill_combat = skill_combat
    #     self.skill_agility = skill_agility
    #     self.play_action_cost = 0
    #     self.is_unique = True
    #     self.is_permanent = True

    #     WithHealthSanity.__init__(self, health, sanity)
