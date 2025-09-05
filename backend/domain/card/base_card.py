from abc import ABC, abstractmethod
from typing import List, Optional

from . import Faction
from . import CardType
from ..models import TabooData


class BaseCard(ABC):

    def __init__(
        self,
        code: str,
        name: str,
        card_type: CardType,
        traits: List[str],
        faction: Faction,
        text: str,
        back_text: Optional[str],
        # cost: int = 0,
        # skill_willpower: int = 0,
        # skill_intellect: int = 0,
        # skill_combat: int = 0,
        # skill_agility: int = 0,
        # play_action_cost: int = 0,
        # is_unique: bool = False,
        # is_permanent: bool = False,
        taboo: Optional[TabooData] = None,
    ):
        self.name = name
        self.card_type = card_type
        self.traits = traits
        self.text = text
        self.back_text = back_text
        self.taboo = taboo

    @classmethod
    def from_dict(cls, data: dict) -> "BaseCard":
        return cls(**data)

    @abstractmethod
    def apply_taboo(self) -> "BaseCard":
        if self.taboo and self.taboo.text:
            self.text += f"\n\n{self.taboo.text}"
        return self

    # @classmethod
    # @abstractmethod
    # def from_(cls, data: dict) -> "BaseCard":
    #     return cls(**data)
