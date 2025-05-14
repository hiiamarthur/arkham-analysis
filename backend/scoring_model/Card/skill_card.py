from typing import List, Optional

from scoring_model.Card import ActivationType, CardType
from scoring_model.Card.player_card import PlayerCard


class SkillCard(PlayerCard):
    def __init__(
        self,
        code: str,
        name: str,
        traits: List[str],
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
        )
