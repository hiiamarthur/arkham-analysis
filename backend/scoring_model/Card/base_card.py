from abc import ABC, abstractmethod
from typing import List, Optional

from scoring_model.Card import CardType
from scoring_model.models import TabooData


class BaseCard(ABC):

    def __init__(
        self,
        code: str,
        name: str,
        card_type: CardType,
        traits: List[str],
        text: str,
        cost: int = 0,
        skill_willpower: int = 0,
        skill_intellect: int = 0,
        skill_combat: int = 0,
        skill_agility: int = 0,
        play_action_cost: int = 0,
        is_unique: bool = False,
        is_permanent: bool = False,
        taboo: Optional[TabooData] = None,
    ):
        self.name = name
        self.card_type = card_type
        self.traits = traits
        self.text = text
        self.cost = cost
        self.skill_willpower = skill_willpower
        self.skill_intellect = skill_intellect
        self.skill_combat = skill_combat
        self.skill_agility = skill_agility
        self.play_action_cost = play_action_cost
        self.is_unique = is_unique
        self.is_permanent = is_permanent

        self.taboo = taboo

    @classmethod
    def from_dict(cls, data: dict) -> "BaseCard":
        return cls(**data)

    @abstractmethod
    def apply_taboo(self) -> "BaseCard":
        if self.taboo and self.taboo.text:
            self.text += f"\n\n{self.taboo.text}"
        return self
