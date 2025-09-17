from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, cast
from dataclasses import dataclass
from typing import Dict, List, Optional, Type


from .faction import Faction
from .card_type import CardType
from domain.models import TabooData

T = TypeVar("T", bound="BaseCard")


class CardMixin:
    """Centralized type registry for dataclass-based cards."""

    _registry: Dict[CardType, Type["BaseCard"]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # If subclass defines a default for `card_type`, use it as registry key
        card_type = getattr(cls, "card_type", None)

        if isinstance(card_type, CardType) and card_type is not CardType.NONE:
            CardMixin._registry[card_type] = cast(Type["BaseCard"], cls)

    @classmethod
    def from_dict(cls, data: dict) -> BaseCard:
        type_name = data.get("card_type")
        if not isinstance(type_name, str):
            raise ValueError(f"Invalid card_type: {type_name}")
        card_type = CardType.from_code(type_name)
        subclass = cls._registry.get(card_type)
        print("subclass", subclass)
        if not subclass:
            raise ValueError(f"Unknown card_type: {type_name}")
        return subclass(**data)


@dataclass
class BaseCard(CardMixin, ABC):
    code: str
    name: str
    traits: List[str]
    faction: Faction
    text: str
    card_type: CardType
    quantity: int = 1
    back_text: Optional[str] = None
    taboo: Optional[TabooData] = None

    @classmethod
    def from_dict(cls, data: dict) -> "BaseCard":
        # Filter data to only include fields that exist in this class
        from dataclasses import fields

        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)

    def apply_taboo(self) -> "BaseCard":
        if self.taboo and self.taboo.text:
            self.text += f"\n\n{self.taboo.text}"
        return self

    @property
    def dict(self) -> dict:
        return self.__dict__

    # @classmethod
    # @abstractmethod
    # def from_(cls, data: dict) -> "BaseCard":
    #     return cls(**data)
