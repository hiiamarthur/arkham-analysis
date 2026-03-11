"""
Chaos token modifications for The Dunwich Legacy.
Source: ArkhamDB campaign expansion pack (dwlc) — scenario reference cards.
Card codes: 02041, 02062, 02118, 02159, 02195, 02236, 02274, 02311.
"""
from typing import Dict, Tuple, Any

DUNWICH_LEGACY_MODIFICATIONS: Dict[str, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]] = {
    # 02041
    "extracurricular_activity": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1. If you fail, discard the top 3 cards of your deck.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2. If you fail, discard the top 5 cards of your deck.",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if there are 10 or more cards in your discard pile).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-1 (-5 instead if there are 10 or more cards in your discard pile).",
                "value": -1,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-X. Discard the top 2 cards of your deck. X is the total printed cost of those discarded cards.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. Discard the top 3 cards of your deck. X is the total printed cost of those discarded cards.",
                "value": "X",
            },
        },
    },

    # 02062
    "the_house_always_wins": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-2. You may spend 2 resources to treat this token as a 0, instead.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. You may spend 3 resources to treat this token as a 0, instead.",
                "value": -3,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-3. If you succeed, gain 3 resources.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, discard 3 resources.",
                "value": -3,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, discard 3 resources.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. Discard 3 resources.",
                "value": -2,
            },
        },
    },

    # 02118
    "the_miskatonic_museum": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if Hunting Horror is at your location).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if Hunting Horror is at your location).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-1. If you fail, search the encounter deck, discard pile, and the void for Hunting Horror and spawn it at your location, if able.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, search the encounter deck, discard pile, and the void for Hunting Horror and spawn it at your location, if able.",
                "value": -3,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. Return 1 of your clues to your current location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. If Hunting Horror is at your location, it immediately attacks you.",
                "value": -4,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, discard an asset you control.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If you fail, discard an asset you control.",
                "value": -5,
            },
        },
    },

    # 02159
    "the_essex_country_express": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the current Agenda #.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is 1 more than the current Agenda #.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-1. If you fail and it is your turn, lose all remaining actions and end your turn immediately.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail and it is your turn, lose all remaining actions and end your turn immediately.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. Add 1 doom token to the nearest Cultist enemy.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. Add 1 doom token to each Cultist enemy in play.",
                "value": -4,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, choose and discard a card from your hand.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, choose and discard a card from your hand for each point you failed by.",
                "value": -3,
            },
        },
    },

    # 02195
    "blood_on_the_altar": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 for each location in play with no encounter card underneath it (max -4).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-1 for each location in play with no encounter card underneath it.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, add 1 clue from the token pool to your location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, add 1 clue from the token pool to your location.",
                "value": -4,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you are in the Hidden Chamber, reveal another token.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. Reveal another token.",
                "value": -3,
                "revealAnotherToken": True,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, place 1 doom on the current agenda.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. Place 1 doom on the current agenda.",
                "value": -3,
            },
        },
    },

    # 02236
    "undimensioned_and_unseen": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 for each Brood of Yog-Sothoth in play.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-2 for each Brood of Yog-Sothoth in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail this test, take 1 horror.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. If you fail this test, take 1 horror and 1 damage.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "0. You must either remove all clue tokens from a Brood of Yog-Sothoth in play, or this token's modifier is -4 instead.",
                "value": 0,
            },
            ("hard", "expert"): {
                "effect": "0. You must either remove all clue tokens from a Brood of Yog-Sothoth in play, or this test automatically fails.",
                "value": 0,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If this token is revealed during an attack or evasion attempt against a Brood of Yog-Sothoth, it immediately attacks you.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If this token is revealed during an attack or evasion attempt against a Brood of Yog-Sothoth, it immediately attacks you.",
                "value": -5,
            },
        },
    },

    # 02274
    "where_doom_awaits": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if you are at an Altered location).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-5 instead if you are at an Altered location).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. Cancel the effects and icons of each skill card committed to this test.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. Cancel the effects and icons of each skill card committed to this test.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2 (-4 instead if it is Agenda 2).",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If it is Agenda 2, you automatically fail instead.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-X. Discard the top 2 cards of your deck. X is the total printed cost of those discarded cards.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. Discard the top 3 cards of your deck. X is the total printed cost of those discarded cards.",
                "value": "X",
            },
        },
    },

    # 02311
    "lost_in_time_and_space": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 for each Extradimensional location in play (max -5).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-1 for each Extradimensional location in play.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "Reveal another token. If you fail, after this skill test, discard cards from the top of the encounter deck until a location is discarded. Put that location into play and move there.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "Reveal another token. After this skill test, discard cards from the top of the encounter deck until a location is discarded. Put that location into play and move there.",
                "value": 0,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If Yog-Sothoth is in play, it attacks you after this skill test.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If Yog-Sothoth is in play, it attacks you after this skill test.",
                "value": -5,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-X. X is the shroud value of your location. If you fail and your location is Extradimensional, discard it.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is twice the shroud value of your location. If you fail and your location is Extradimensional, discard it.",
                "value": "X",
            },
        },
    },
}
