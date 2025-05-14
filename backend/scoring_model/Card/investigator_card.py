from typing import List
from scoring_model.Card import CardType
from scoring_model.Card.base_card import BaseCard

from scoring_model.Card.with_health_sanity import WithHealthSanity


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
        faction: str,
        health: int,
        sanity: int,
    ):
        super().__init__(
            code,
            name,
            CardType.INVESTIGATOR,
            traits,
            text,
            skill_willpower,
            skill_intellect,
            skill_combat,
            skill_agility,
            is_unique=True,
            is_permanent=True,
        )
        WithHealthSanity.__init__(self, health, sanity)
        self.faction = faction
