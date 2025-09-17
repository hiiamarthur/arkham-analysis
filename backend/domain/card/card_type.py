from enum import Enum
from typing import List


class CardType(Enum):
    """Card types in Arkham Horror LCG"""

    ASSET = "asset"
    EVENT = "event"
    SKILL = "skill"
    INVESTIGATOR = "investigator"
    ENEMY = "enemy"
    TREACHERY = "treachery"
    LOCATION = "location"
    ACT = "act"
    AGENDA = "agenda"
    STORY = "story"
    SCENARIO = "scenario"
    NONE = "none"

    @property
    def display_name(self) -> str:
        """Human-readable card type name"""
        return self.value.title()

    @property
    def is_player_card(self) -> bool:
        """Check if this is a player card type"""
        return self in {
            CardType.ASSET,
            CardType.EVENT,
            CardType.SKILL,
            CardType.INVESTIGATOR,
        }

    @property
    def is_encounter_card(self) -> bool:
        """Check if this is an encounter card type"""
        return self in {
            CardType.ENEMY,
            CardType.TREACHERY,
            CardType.LOCATION,
            CardType.ACT,
            CardType.AGENDA,
            CardType.STORY,
        }

    @classmethod
    def player_cards(cls) -> List["CardType"]:
        """Get all player card types"""
        return [card_type for card_type in cls if card_type.is_player_card]

    @classmethod
    def encounter_cards(cls) -> List["CardType"]:
        """Get all encounter card types"""
        return [card_type for card_type in cls if card_type.is_encounter_card]

    @classmethod
    def all_cards(cls) -> List["CardType"]:
        """Get all card types"""
        return list(cls)

    @classmethod
    def from_code(cls, code: str) -> "CardType":
        """Get card type from code, returns None if not found"""
        try:
            print(f"Getting card type from code: {code}")
            print(f"Card type: {cls(code)}")
            return cls(code)
        except ValueError:
            print(f"Error getting card type from code: {code}")
            return CardType.NONE

    def __str__(self) -> str:
        return self.display_name
