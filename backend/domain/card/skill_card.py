from typing import List, Optional

from . import ActivationType, CardCostFactor, CardType
from .player_card import PlayerCard
from . import Faction


class SkillCard(PlayerCard):
    def __init__(
        self,
        code: str,
        name: str,
        traits: List[str],
        faction: Faction,
        text: str,
        level: int = 0,
        skill_willpower: int = 0,
        skill_intellect: int = 0,
        skill_combat: int = 0,
        skill_agility: int = 0,
        skill_wild: int = 0,
    ):
        super().__init__(
            code,
            name,
            CardType.SKILL,
            traits,
            faction,
            text,
            0,
            level,
            skill_willpower,
            skill_intellect,
            skill_combat,
            skill_agility,
            skill_wild,
            play_action_cost=0,
            activation_type=ActivationType.FAST,
            cost_factors={
                CardCostFactor.ACTION: 0,
                CardCostFactor.RESOURCE: 0,
                CardCostFactor.ICON: 0,
                CardCostFactor.XP: 1,
            },
        )
