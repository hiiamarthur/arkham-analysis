"""
Chaos token modifications for The Forgotten Age.
Source: ArkhamDB campaign expansion pack (tfac) — scenario reference cards.
Card codes: 04043, 04054, 04113, 04161, 04205, 04237, 04277, 04314, 04344.
"""
from typing import Dict, Tuple, Any

FORGOTTEN_AGE_MODIFICATIONS: Dict[str, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]] = {
    # 04043
    "the_untamed_wilds": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of vengeance points in the victory display.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is 1 higher than the number of vengeance points in the victory display.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of locations in play (max 5).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the number of locations in play.",
                "value": "X",
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of cards in the exploration deck (max 5).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the number of cards in the exploration deck (min 3).",
                "value": "X",
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you are poisoned, this test automatically fails instead.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you are poisoned, this test automatically fails instead. If you are not poisoned and you fail, put a set-aside Poisoned weakness into play in your threat area.",
                "value": -3,
            },
        },
    },

    # 04054 — cultist and tablet share effects
    "the_doom_of_eztli": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if there is doom on your location).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if there is doom on your location).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of locations with doom on them.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total amount of doom on locations in play.",
                "value": "X",
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of locations with doom on them.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total amount of doom on locations in play.",
                "value": "X",
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "Reveal another chaos token. If you fail, place 1 doom on your location.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another chaos token. Place 1 doom on your location.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
    },

    # 04113
    "threads_of_fate": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the highest number of doom on a Cultist enemy.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total number of doom in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you do not succeed by at least 1, take 1 damage.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. If you do not succeed by at least 2, take 1 direct damage.",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you do not succeed by at least 1, place 1 doom on the nearest Cultist enemy.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. If you do not succeed by at least 2, place 1 doom on each Cultist enemy.",
                "value": -2,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, lose 1 of your clues.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, lose 1 of your clues.",
                "value": -3,
            },
        },
    },

    # 04161
    "the_boundary_beyond": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if you are at an Ancient location).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if you are at an Ancient location).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, place 1 doom on a Cultist enemy.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, place 1 doom on each Cultist enemy.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail and there is a Serpent enemy at your location, it attacks you.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, each Serpent enemy at your location attacks you.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, place 1 clue (from the token pool) on the nearest Ancient location.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-4. Place 1 clue (from the token pool) on the nearest Ancient location.",
                "value": -4,
            },
        },
    },

    # 04205
    "heart_of_the_elders": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if you are in a Cave location).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if you are in a Cave location).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, place 1 doom on your location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, place 1 doom on your location.",
                "value": -3,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you are poisoned, this test automatically fails instead.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you are poisoned, this test automatically fails instead. If you are not poisoned and you fail, put a set-aside Poisoned weakness into play in your threat area.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, take 1 horror.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, take 1 horror.",
                "value": -4,
            },
        },
    },

    # 04237 — cultist and elder_thing share effects
    "the_city_of_archives": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if you have 5 or more cards in your hand).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (if you have 5 or more cards in your hand, you automatically fail instead).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, place 1 of your clues on your location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. Place 1 of your clues on your location.",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, discard 1 random card from your hand.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. For each point you fail by, discard 1 random card from your hand.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, place 1 of your clues on your location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. Place 1 of your clues on your location.",
                "value": -2,
            },
        },
    },

    # 04277
    "the_depths_of_yoth": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the current depth level.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the current depth level. If you fail, take 1 horror.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, each Serpent enemy at your location or a connecting location heals 2 damage.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, each Serpent enemy at your location or a connecting location heals 2 damage.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, place 1 clue on your location (from the token pool).",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, place 1 clue on your location (from the token pool).",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If there are 3 or more vengeance points in the victory display, you automatically fail this test, instead.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. If there are 3 or more vengeance points in the victory display, you automatically fail this test, instead.",
                "value": -4,
            },
        },
    },

    # 04314
    "shattered_aeons": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-2 (-4 instead if the Relic of Ages is at your location).",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3 (-5 instead if the Relic of Ages is at your location).",
                "value": -3,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you do not succeed by at least 1, place 1 doom on the nearest Cultist enemy.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you do not succeed by at least 1, place 1 doom on each Cultist enemy.",
                "value": -3,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you are poisoned, this test automatically fails instead.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you are poisoned, this test automatically fails instead. If you are not poisoned and you fail, put a set-aside Poisoned weakness into play in your threat area.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, shuffle the topmost Hex treachery in the encounter discard pile into the exploration deck.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. Shuffle the topmost Hex treachery in the encounter discard pile into the exploration deck.",
                "value": -3,
            },
        },
    },

    # 04344 — only skull and elder_thing listed
    "turn_back_time": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of locations with doom on them.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total amount of doom on locations.",
                "value": "X",
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, place 1 doom on your location.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-6. Place 1 doom on your location.",
                "value": -6,
            },
        },
    },
}
