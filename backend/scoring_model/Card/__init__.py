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


class CardCostFactor(Enum):
    ACTION = "action"
    RESOURCE = "resource"
    ICON = "icon"
    XP = "xp"


class CardEffect(Enum):
    ACTION = "action"
    RESOURCE = "resource"
    CARD = "card"
    DAMAGE = "damage"
    CLUE = "clue"
    ICON = "icon"
    HORROR = "horror"
    HEALTH = "health"
    USE = "use"
    MOVE = "move"
    DOOM = "doom"
    FAST = "fast"
    REACTION = "reaction"
    EXHAUST = "exhaust"
    BLESSED = "blessed"
    CURSED = "cursed"
    SEALED = "sealed"
    ENCOUNTER = "encounter"
    ENEMY = "enemy"
    XP = "xp"
