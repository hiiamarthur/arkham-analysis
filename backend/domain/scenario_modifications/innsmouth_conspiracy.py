"""
Chaos token modifications for The Innsmouth Conspiracy.
Source: ArkhamDB campaign expansion pack (ticc) — scenario reference cards.
Card codes: 07041, 07056, 07123, 07163, 07198, 07231, 07274, 07311.

Note: This campaign features flooding mechanics (partially/fully flooded locations),
      keys, barriers, Deep One enemies, vehicle checks, and curse tokens.
"""
from typing import Dict, Tuple, Any

INNSMOUTH_CONSPIRACY_MODIFICATIONS: Dict[str, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]] = {
    # 07041
    "the_pit_of_despair": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-2 instead if your location is partially flooded; -3 instead if your location is fully flooded).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-3 instead if your location is partially flooded; -4 instead if your location is fully flooded).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail and your location is flooded, take 1 damage.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. If your location is flooded, take 1 damage.",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. If you fail and you control a key, take 1 horror.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. If you control a key, take 1 horror.",
                "value": -2,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-3. If you fail and The Amalgam is in the depths, put it into play engaged with you.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. If The Amalgam is in the depths, put it into play engaged with you.",
                "value": -3,
            },
        },
    },

    # 07056
    "the_vanishing_of_elina_harper": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the current agenda number.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is 1 more than the current agenda number.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, place 1 doom on the nearest enemy.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. Place 1 doom on the nearest enemy (2 doom instead if you failed).",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, take 1 horror.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. Take 1 horror (1 horror and 1 damage instead if you failed).",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, place 1 of your clues on your location.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-4. Place 1 of your clues on your location (2 clues instead if you failed).",
                "value": -4,
            },
        },
    },

    # 07123
    "in_too_deep": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 for each location to the east of your location (on the same row).",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-2 for each location to the east of your location (on the same row).",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, move to the connecting location to the east, ignoring all barriers.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, move to the connecting location to the east, ignoring all barriers.",
                "value": -4,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, choose a connecting location with no barriers between it and your location. Place 1 barrier between the two locations.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If you fail, choose a connecting location with no barriers between it and your location. Place 1 barrier between the two locations.",
                "value": -5,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of barriers between your location and all connecting locations.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is twice the number of barriers between your location and all connecting locations.",
                "value": "X",
            },
        },
    },

    # 07163
    "devil_reef": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of keys the investigators control.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is 1 more than the number of keys the investigators control.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail and this is an attack or evasion attempt against a Deep One enemy, it engages you. (If it is already engaged with you, it disengages first, then re-engages you.)",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. If this is an attack or evasion attempt against a Deep One enemy, it engages you. (If it is already engaged with you, it disengages first, then re-engages you.)",
                "value": -3,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail and you are not in a vehicle, take 1 damage.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you are not in a vehicle, take 1 damage.",
                "value": -4,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If you fail and your location has a key on it, take 1 horror.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-5. If your location has a key on it, take 1 horror.",
                "value": -5,
            },
        },
    },

    # 07198
    "horror_in_high_gear": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if there are 6 or fewer locations remaining in the Road deck).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if there are 6 or fewer locations remaining in the Road deck).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-1. For each point you fail by, an investigator in your vehicle places 1 of their clues on your location.",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2. For each point you fail by, an investigator in your vehicle places 1 of their clues on your location.",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-2. For each point you fail by, an investigator in your vehicle loses 1 resource.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-3. For each point you fail by, an investigator in your vehicle loses 1 resource.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, resolve the hunter keyword on each enemy in play.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-4. Resolve the hunter keyword on each enemy in play.",
                "value": -4,
            },
        },
    },

    # 07231
    "a_light_in_the_fog": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1. If your location is flooded, reveal an additional chaos token.",
                "value": -1,
                "revealAnotherToken": False,  # conditional on location state
            },
            ("hard", "expert"): {
                "effect": "-2. If your location is flooded, reveal an additional chaos token.",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. If you fail, after this test ends, increase the flood level of your location.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-2. If you fail, after this test ends, increase the flood level of your location (if you cannot, take 1 horror instead).",
                "value": -2,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail this test and your location is flooded, take 1 damage.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail this test and your location is flooded, take 2 damage.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, move the nearest ready unengaged enemy once toward your location. It loses aloof during this movement.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-4. Move the nearest unengaged enemy once toward your location. It loses aloof during this movement.",
                "value": -4,
            },
        },
    },

    # 07274
    "the_lair_of_dagon": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 for each key on this card.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-2 for each key on this card.",
                "value": "X",
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "0. Reveal an additional chaos token. If you reveal 1 or more curse tokens during this test, you automatically fail.",
                "value": 0,
                "revealAnotherToken": True,
            },
            ("hard", "expert"): {
                "effect": "-2. Reveal an additional chaos token. If you reveal 1 or more curse tokens during this test, you automatically fail.",
                "value": -2,
                "revealAnotherToken": True,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, place each key you control on your location.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. Place each key you control on your location and take 1 damage.",
                "value": -3,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, add 1 curse token to the chaos bag.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-4. Add 2 curse tokens to the chaos bag.",
                "value": -4,
            },
        },
    },

    # 07311
    "into_the_maelstrom": {
        "skull": {
            ("easy", "standard"): {
                "effect": "-1 (-3 instead if there are 4 or more unflooded Y'ha-nthlei locations in play).",
                "value": -1,
            },
            ("hard", "expert"): {
                "effect": "-2 (-4 instead if there are 4 or more unflooded Y'ha-nthlei locations in play).",
                "value": -2,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-3. If you fail, place 1 doom on the current agenda (this may cause the current agenda to advance).",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-4. If you fail, place 1 doom on the current agenda (this may cause the current agenda to advance).",
                "value": -4,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-4. If you fail, you must either increase the flood level of your location or take 1 damage.",
                "value": -4,
            },
            ("hard", "expert"): {
                "effect": "-5. If you fail, you must either increase the flood level of your location or take 1 damage.",
                "value": -5,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-5. If you fail and there is a key on your location, take 1 horror.",
                "value": -5,
            },
            ("hard", "expert"): {
                "effect": "-6. If you fail and there is a key on your location, take 1 horror.",
                "value": -6,
            },
        },
    },
}
