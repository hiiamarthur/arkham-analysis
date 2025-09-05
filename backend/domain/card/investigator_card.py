from typing import List

from . import Faction
from . import CardType
from .base_card import BaseCard
from .with_health_sanity import WithHealthSanity


class InvestigatorCard(BaseCard, WithHealthSanity):
    def __init__(
        self,
        code: str,
        name: str,
        traits: List[str],
        text: str,
        skill_willpower: int,
        skill_intellect: int,
        skill_combat: int,
        skill_agility: int,
        faction: Faction,
        health: int,
        sanity: int,
    ):
        super().__init__(
            code,
            name,
            CardType.INVESTIGATOR,
            traits,
            faction,
            text,
            "",
        )
        self.skill_willpower = skill_willpower
        self.skill_intellect = skill_intellect
        self.skill_combat = skill_combat
        self.skill_agility = skill_agility
        self.play_action_cost = 0
        self.is_unique = True
        self.is_permanent = True

        WithHealthSanity.__init__(self, health, sanity)
