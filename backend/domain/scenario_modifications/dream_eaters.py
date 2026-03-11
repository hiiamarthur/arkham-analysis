"""
Chaos token modifications for The Dream-Eaters.
Source: ArkhamDB campaign expansion pack (tdec) — scenario reference cards.
Card codes: 06039, 06063, 06119, 06168, 06206, 06247, 06286, 06333.

Note: Several scenarios feature a positive elder_thing token ("The black cat...")
      which is unique to this campaign.
"""
from typing import Dict, Tuple, Any

DREAM_EATERS_MODIFICATIONS: Dict[str, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]] = {
    # 06039
    "beyond_the_gates_of_sleep": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is half the number of cards in your hand (rounded up).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the number of cards in your hand.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of revealed Enchanted Woods locations.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the number of revealed Woods locations.",
                "value": "X",
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you fail and this is an attack or evasion attempt against a swarming enemy, add 1 swarm card to it.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. If this is an attack or evasion attempt against a swarming enemy, add 1 swarm card to it.",
                "value": -2,
            },
        },
    },

    # 06063
    "waking_nightmare": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if you are engaged with a Staff enemy).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if you are engaged with a Staff enemy).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another chaos token. If you fail and it is agenda 2 or 3, make an infestation test.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another chaos token. If it is agenda 2 or 3, make an infestation test.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of infested locations.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is 1 higher than the number of infested locations.",
                "value": "X",
            },
        },
    },

    # 06119
    "the_search_for_kadath": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of Signs of the Gods the investigators have uncovered.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is 1 more than the number of Signs of the Gods the investigators have uncovered.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If this token is revealed during an investigation and this skill test fails, increase that location's shroud by 1 for the remainder of the round.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If this token is revealed during an investigation and this skill test fails, increase that location's shroud by 2 for the remainder of the round.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, either take 1 damage and 1 horror, or place 1 doom on the current agenda.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, either take 1 damage and 1 horror, or place 1 doom on the current agenda.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "+2. The black cat points you in the right direction. If this token is revealed during an investigation and you succeed, discover 1 additional clue.",
                "value": 2,
            },
            ("hard", "expert"): {
                "effect": "+1. The black cat points you in the right direction. If this token is revealed during an investigation and you succeed, discover 1 additional clue.",
                "value": 1,
            },
        },
    },

    # 06168
    "a_thousand_shapes_of_horror": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if you are at a Graveyard location).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if you are at a Graveyard location).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail and The Unnamable is in play, it attacks you (regardless of its current location).",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail and The Unnamable is in play, it attacks you (regardless of its current location).",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "+2. The black cat causes a distraction. If this test is successful, choose and evade an enemy at any location with a fight value of X or lower, where X is the amount you succeeded by.",
                "value": 2,
            },
            ("hard", "expert"): {
                "effect": "+1. The black cat causes a distraction. If this test is successful, choose and evade an enemy at any location with a fight value of X or lower, where X is the amount you succeeded by.",
                "value": 1,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, you must either place 1 of your clues on your location or take 1 damage.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, you must either place 1 of your clues on your location or take 1 damage.",
                "value": -3,
            },
        },
    },

    # 06206
    "dark_side_of_the_moon": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is half your alarm level (rounded up).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is your alarm level.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail and your alarm level is higher than your modified skill value, after this skill test ends, draw the top card of the encounter deck.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail and your alarm level is higher than your modified skill value, after this skill test ends, draw the top card of the encounter deck.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-1. If you fail, raise your alarm level by 1.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2. If you fail, raise your alarm level by 1.",
                "value": -2,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "+1. The black cat summons several other cats to help. If this token is revealed during an evasion attempt and you succeed, deal 2 damage to the evaded enemy.",
                "value": 1,
            },
            ("hard", "expert"): {
                "effect": "0. The black cat summons several other cats to help. If this token is revealed during an evasion attempt and you succeed, deal 2 damage to the evaded enemy.",
                "value": 0,
            },
        },
    },

    # 06247
    "point_of_no_return": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the amount of damage on this card.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is 1 more than the amount of damage on this card.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, after this skill test ends, draw the top card of the encounter deck.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, after this skill test ends, draw the top card of the encounter deck.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "+1. The black cat helps you navigate through the death-fire. If this token is revealed during an investigation and you succeed, draw 1 card.",
                "value": 1,
            },
            ("hard", "expert"): {
                "effect": "0. The black cat helps you navigate through the death-fire. If this token is revealed during an investigation and you succeed, draw 1 card.",
                "value": 0,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail by 2 or more, choose a ready enemy at your location or a connecting location. That enemy moves to your location, engages you, and makes an immediate attack.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail by 2 or more, choose a ready enemy at your location or a connecting location. That enemy moves to your location, engages you, and makes an immediate attack.",
                "value": -4,
            },
        },
    },

    # 06286
    "where_the_gods_dwell": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of the current act.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the number of the current act plus the number of the current agenda.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, place 1 doom on the current agenda.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, place 1 doom on the current agenda. This effect may cause the current agenda to advance.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, choose and reveal a copy of Nyarlathotep in your hand. It attacks you and is shuffled into the encounter deck.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-6. If you fail, choose and reveal a copy of Nyarlathotep in your hand. It attacks you and is shuffled into the encounter deck.",
                "value": -6,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "0. The black cat reminds you that it's all a dream.",
                "value": 0,
            },
            ("hard", "expert"): {
                "effect": "-1. The black cat reminds you that it's all a dream.",
                "value": -1,
            },
        },
    },

    # 06333
    "weaver_of_the_cosmos": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the highest amount of doom on a location in play.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the amount of doom on locations in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, and there is an Ancient One enemy at your location, it attacks you.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, and there is an Ancient One enemy at your location, it attacks you.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "0. The black cat tears at the web with its claws. If you succeed by 2 or more, remove 1 doom from your location.",
                "value": 0,
            },
            ("hard", "expert"): {
                "effect": "-1. The black cat tears at the web with its claws. If you succeed by 2 or more, remove 1 doom from your location.",
                "value": -1,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If this skill test fails during an attack against a Spider enemy, place 1 doom on that enemy's location.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If this skill test fails during an attack against a Spider enemy, place 1 doom on that enemy's location.",
                "value": -4,
            },
        },
    },
}
