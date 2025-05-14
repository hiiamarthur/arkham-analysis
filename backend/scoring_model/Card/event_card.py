from typing import List, Optional
from scoring_model.Card import ActivationType, CardType
from scoring_model.Card.player_card import PlayerCard


class EventCard(PlayerCard):
    def __init__(
        self,
        code: str,
        name: str,
        traits: List[str],
        text: str,
        cost: int,
        level: int = 0,
        skill_willpower: int = 0,
        skill_intellect: int = 0,
        skill_combat: int = 0,
        skill_agility: int = 0,
        skill_wild: int = 0,
        play_action_cost: int = 1,
        is_unique: bool = False,
        is_permanent: bool = False,
        is_exceptional: bool = False,
        activation_type: ActivationType = ActivationType.PLAY,
    ):
        super().__init__(
            code,
            name,
            CardType.EVENT,
            traits,
            text,
            cost,
            level,
            skill_willpower,
            skill_intellect,
            skill_combat,
            skill_agility,
            skill_wild,
            play_action_cost,
            is_unique,
            is_permanent,
            is_exceptional,
            activation_type,
        )
