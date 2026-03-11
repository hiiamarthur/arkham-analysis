"""
Chaos token modifications for The Path to Carcosa.
Source: ArkhamDB campaign expansion pack (ptcc) — scenario reference cards.
Card codes: 03043, 03061, 03120, 03159, 03200, 03240, 03274, 03316.
"""
from typing import Dict, Tuple, Any

PATH_TO_CARCOSA_MODIFICATIONS: Dict[str, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]] = {
    # 03043 — cultist/tablet/elder_thing share identical effects
    "curtain_call": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if you have 3 or more horror on you).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-X, where X is the amount of horror on you. (If you have no horror on you, X is 1.)",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-4. If your location has at least 1 horror on it, take 1 horror. If your location has no horror on it, place 1 horror on it instead.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-5. If your location has at least 1 horror on it, take 1 horror. If your location has no horror on it, place 1 horror on it instead.",
                "value": -5,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-4. If your location has at least 1 horror on it, take 1 horror. If your location has no horror on it, place 1 horror on it instead.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-5. If your location has at least 1 horror on it, take 1 horror. If your location has no horror on it, place 1 horror on it instead.",
                "value": -5,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If your location has at least 1 horror on it, take 1 horror. If your location has no horror on it, place 1 horror on it instead.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-5. If your location has at least 1 horror on it, take 1 horror. If your location has no horror on it, place 1 horror on it instead.",
                "value": -5,
            },
        },
    },

    # 03061
    "the_last_king": {
        "skull": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, place 1 doom on a Possessed enemy in play.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, place 1 doom on the Possessed enemy in play with the most remaining health.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, place 1 of your clues on your location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. Place 1 of your clues on your location.",
                "value": -3,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, take 1 horror.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-4. Take 1 horror.",
                "value": -4,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-X. X is the shroud value of your location.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the shroud value of your location. If you fail, take 1 damage.",
                "value": "X",
            },
        },
    },

    # 03120
    "echoes_of_the_past": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the highest number of doom on an enemy in play.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total number of doom on enemies in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, place 1 doom on the nearest enemy.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. Place 1 doom on the nearest enemy.",
                "value": -4,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, discard a random card from your hand.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. Discard a random card from your hand.",
                "value": -4,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you fail and there is an enemy at your location, take 1 horror.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. If there is an enemy at your location, take 1 horror.",
                "value": -4,
            },
        },
    },

    # 03159
    "the_unspeakable_oath": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1. If you fail, randomly choose an enemy from among the set-aside Monster enemies and place it beneath the act deck without looking at it.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, randomly choose an enemy from among the set-aside Monster enemies and place it beneath the act deck without looking at it. (Limit once per test.)",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-X. X is the amount of horror on you.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the amount of horror on you. If you fail, take 1 horror.",
                "value": "X",
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-X. X is the base shroud value of your location.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the base shroud value of your location. If you fail, take 1 horror.",
                "value": "X",
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "0. Either randomly choose an enemy from among the set-aside Monster enemies and place it beneath the act deck without looking at it, or this test automatically fails instead.",
                "value": 0,
            },
            ("hard", "expert"): {
                "effect": "0. Either randomly choose an enemy from among the set-aside Monster enemies and place it beneath the act deck without looking at it, or this test automatically fails instead.",
                "value": 0,
            },
        },
    },

    # 03200
    "a_phantom_of_truth": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the amount of doom in play (max 5).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the amount of doom in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, move each unengaged Byakhee in play once toward the nearest investigator.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. Move each unengaged Byakhee in play once toward the nearest investigator.",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. Cancel the effects and icons of each skill card committed to this test.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. Cancel the effects and icons of each skill card committed to this test.",
                "value": -4,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, lose 1 resource for each point you failed by.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, lose 1 resource for each point you failed by.",
                "value": -3,
            },
        },
    },

    # 03240
    "the_pallid_mask": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of locations away from the starting location you are (max 5).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the number of locations away from the starting location you are.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If this token is revealed during an attack, and this skill test is successful, this attack deals 1 less damage.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If this token is revealed during an attack and this skill test is successful, this attack deals no damage.",
                "value": -3,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If there is a ready Ghoul or Geist enemy at your location, it attacks you.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If there is a Ghoul or Geist enemy at your location, it readies and attacks you.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, search the encounter deck and discard pile for a Ghoul or Geist enemy and draw it.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, search the encounter deck and discard pile for a Ghoul or Geist enemy and draw it.",
                "value": -4,
            },
        },
    },

    # 03274
    "black_stars_rise": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the highest amount of doom on an agenda in play.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total amount of doom on agendas in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If this token is revealed during an attack or evasion attempt against an enemy with doom on it, this skill test automatically fails instead.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If there is an enemy with 1 or more doom on it at your location, this test automatically fails instead.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, place 1 doom on each agenda.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you do not succeed by at least 1, place 1 doom on each agenda.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, search the encounter deck and discard pile for a Byakhee enemy and draw it.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, search the encounter deck and discard pile for a Byakhee enemy and draw it.",
                "value": -3,
            },
        },
    },

    # 03316
    "dim_carcosa": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-2 (-4 instead if you have no sanity remaining).",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-X. X is the amount of horror on you.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, take 1 horror.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail, take 2 horror.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail and Hastur is in play, place 1 clue on your location.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If you fail and Hastur is in play, place 1 clue on your location.",
                "value": -5,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If this token is revealed during an attack or evasion attempt against a Monster or Ancient One enemy, lose 1 action.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If this token is revealed during an attack or evasion attempt against a Monster or Ancient One enemy, lose 1 action.",
                "value": -5,
            },
        },
    },
}
