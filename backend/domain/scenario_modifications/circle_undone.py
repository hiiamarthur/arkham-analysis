"""
Chaos token modifications for The Circle Undone.
Source: ArkhamDB campaign expansion pack (tcuc) — scenario reference cards.
Card codes: 05043, 05050, 05065, 05120, 05161, 05197, 05238, 05284, 05325.

Note: Several scenarios in this campaign only define effects for a subset of
special tokens — missing tokens are not present on the reference card.
"""
from typing import Dict, Tuple, Any

CIRCLE_UNDONE_MODIFICATIONS: Dict[str, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]] = {
    # 05043 — only skull token listed
    "disappearance_at_the_twilight_estate": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-3. If you fail and this is an attack or evasion attempt, resolve each haunted ability on your location.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If you fail and this is an attack or evasion attempt, resolve each haunted ability on your location.",
                "value": -5,
            },
        },
    },

    # 05050 — skull, tablet, elder_thing (no cultist)
    "the_witching_hour": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1. For each point you fail by, discard the top card of the encounter deck.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2. Discard cards from the top of the encounter deck equal to this test's difficulty.",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-1. If you fail, after this test resolves, draw the bottommost treachery in the encounter discard pile.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2. If you fail, after this test resolves, draw the bottommost treachery in the encounter discard pile.",
                "value": -2,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, choose an exhausted or damaged Witch enemy at your location or at a connecting location. Ready that enemy and heal all damage from it.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, ready each Witch enemy at your location and at each connecting location. Heal all damage from each of those enemies.",
                "value": -4,
            },
        },
    },

    # 05065 — skull, tablet, elder_thing (no cultist)
    "at_deaths_doorstep": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if your location is haunted).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if your location is haunted).",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you fail and this is an attack or evasion attempt, resolve each haunted ability on your location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If this is an attack or evasion attempt, resolve each haunted ability on your location.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If there is a Spectral enemy at your location, take 1 damage.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. If there is a Spectral enemy at your location, take 1 damage and 1 horror.",
                "value": -4,
            },
        },
    },

    # 05120
    "the_secret_name": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if you are at an Extradimensional location).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if you are at an Extradimensional location).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another chaos token. If you fail, discard the top 3 cards of the encounter deck.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another chaos token. If you fail, discard the top 5 cards of the encounter deck.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you fail and Nahab is at your location, she attacks you.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail and Nahab is in play, she attacks you (regardless of her current location).",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, resolve the hunter keyword on each enemy in play.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. Resolve the hunter keyword on each enemy in play.",
                "value": -4,
            },
        },
    },

    # 05161
    "the_wages_of_sin": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is 1 higher than the number of copies of Unfinished Business in the victory display.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the number of copies of Unfinished Business in the victory display. Reveal another token.",
                "value": "X",
                "revealAnotherToken": True,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-3. Until the end of the round, each Heretic enemy in play gets +1 fight and +1 evade.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. Until the end of the round, each Heretic enemy in play gets +1 fight and +1 evade.",
                "value": -4,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, trigger the forced ability on a copy of Unfinished Business in your threat area as if it were the end of the round.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, trigger the forced ability on a copy of Unfinished Business in your threat area as if it were the end of the round.",
                "value": -4,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you fail and this is an attack or evasion attempt, resolve each haunted ability on your location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. If this is an attack or evasion attempt, resolve each haunted ability on your location.",
                "value": -2,
            },
        },
    },

    # 05197
    "for_the_greater_good": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the highest number of doom on a Cultist enemy in play.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total number of doom among Cultist enemies in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. Reveal another token.",
                "value": -2,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "-2. Reveal another token.",
                "value": -2,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, place 1 doom on the nearest Cultist enemy.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, place 1 doom on each Cultist enemy in play. If there are no Cultist enemies in play, reveal another token.",
                "value": -3,
                "revealAnotherToken": True,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, move 1 doom from the nearest Cultist enemy to the current agenda.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, move all doom from the Cultist enemy with the most doom on it to the current agenda. If no Cultist enemies in play have doom on them, reveal another token.",
                "value": -3,
                "revealAnotherToken": True,
            },
        },
    },

    # 05238
    "union_and_disillusion": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-2. If this is a skill test during a circle action, reveal another token.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If this is a skill test during a circle action, reveal another token.",
                "value": -3,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-3. If you have no damage on you, take 1 damage. If you have no horror on you, take 1 horror.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you have no damage on you, take 1 damage. If you have no horror on you, take 1 horror.",
                "value": -4,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, a Spectral enemy at your location attacks you (even if it is exhausted).",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, a Spectral enemy at your location attacks you (even if it is exhausted).",
                "value": -4,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If this is a skill test during a circle action and you fail, resolve each haunted ability on your location.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If this is a skill test during a circle action and you fail, resolve each haunted ability on your location.",
                "value": -4,
            },
        },
    },

    # 05284
    "in_the_clutches_of_chaos": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the total amount of doom and breaches on your location.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is 1 higher than the total amount of doom and breaches on your location.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If there are fewer than 3 breaches on your location, place 1 breach on your location.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If there are fewer than 3 breaches on your location, place 1 breach on your location.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. For each point you fail by, remove 1 breach from the current act.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. For each point you fail by, remove 1 breach from the current act.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, place 1 breach on a random location.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, place 1 breach on a random location.",
                "value": -4,
            },
        },
    },

    # 05325
    "before_the_black_throne": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is half of the doom on Azathoth (rounded up), to a minimum of 2.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the amount of doom on Azathoth, to a minimum of 2.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, search the encounter deck and discard pile for a Cultist enemy and draw it. Shuffle the encounter deck.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, search the encounter deck and discard pile for a Cultist enemy and draw it. Shuffle the encounter deck.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, Azathoth attacks you.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, Azathoth attacks you.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If your modified skill value for this test is 0, place 1 doom on Azathoth.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-6. If your modified skill value for this test is 0, place 1 doom on Azathoth.",
                "value": -6,
            },
        },
    },
}
