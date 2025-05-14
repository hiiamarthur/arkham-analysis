from enum import Enum


class CardType(Enum):
    INVESTIGATOR = "investigator"
    ASSET = "asset"
    EVENT = "event"
    SKILL = "skill"


class ActivationType(Enum):
    ACTION = "Action"
    PLAY = "Play"
    FAST = "Fast"
    REACTION = "Reaction"
    FORCED = "Forced"
    PASSIVE = "Passive"
