from enum import Enum


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
