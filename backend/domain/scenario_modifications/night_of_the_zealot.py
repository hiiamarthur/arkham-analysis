"""
Chaos token modifications for Night of the Zealot (Core Set).
Source: ArkhamDB — scenario reference cards (core set predates API tracking;
        effects sourced from official printed cards).
"""
from typing import Dict, Tuple, Any

NIGHT_OF_THE_ZEALOT_MODIFICATIONS: Dict[str, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]] = {
    "the_gathering": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of Ghoul enemies at your location.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-2. If you fail, after this skill test, search the encounter deck and discard pile for a Ghoul enemy, and draw it. Shuffle the encounter deck.",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-1. If you fail, take 1 horror.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, take 2 horror.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If there is a Ghoul enemy at your location, take 1 damage.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. If there is a Ghoul enemy at your location, take 1 damage and 1 horror.",
                "value": -4,
            },
        },
    },

    "the_midnight_masks": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the highest number of doom on a Cultist enemy in play.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total number of doom in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. Place 1 doom on the nearest Cultist enemy.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. Place 1 doom on each Cultist enemy in play. If there are no Cultist enemies in play, reveal another token.",
                "value": -2,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, place 1 of your clues on your location.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, place all your clues on your location.",
                "value": -4,
            },
        },
    },

    "the_devourer_below": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of Cultist enemies at your location.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the number of Cultist enemies at your location. If there are none, reveal another token.",
                "value": "X",
                "revealAnotherToken": True,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, place 1 doom on the nearest Cultist enemy.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. Place 1 doom on each Cultist enemy in play. If there are no Cultist enemies in play, reveal another token.",
                "value": -2,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, place 1 doom on the current agenda.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If you fail, place 1 doom on the current agenda.",
                "value": -5,
            },
        },
    },
}
