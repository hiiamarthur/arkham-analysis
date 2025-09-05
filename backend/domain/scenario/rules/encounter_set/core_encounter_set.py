from domain import ScenarioType


CORE_ENCOUNTER_SET = {
    # Core Set Encounter Sets
    "ancient_evils": {
        "name": "Ancient Evils",
        "icon": "ancient_evils",
        "scenarios": [
            # Night of the Zealot
            ScenarioType.THE_GATHERING,
            ScenarioType.THE_DEVOURER_BELOW,
            # Dunwich Legacy
            ScenarioType.EXTRACURRICULAR_ACTIVITIES,
            ScenarioType.THE_ESSEX_COUNTRY_EXPRESS,
            ScenarioType.BLOOD_ON_THE_ALTAR,
            ScenarioType.WHERE_DOOM_AWAITS,
            # Path to Carcosa
            ScenarioType.THE_LAST_KING,
            ScenarioType.BLACK_STAR_RISE,
            # Forgotten Age
            ScenarioType.THE_UNTAMED_WILDS,
            ScenarioType.SHATTERED_AEONS,
            # Circle Undone
            ScenarioType.THE_WITCHING_HOUR,
            ScenarioType.FOR_THE_GREATER_GOOD,
            ScenarioType.UNION_AND_DISILLUSION,
            ScenarioType.BEFORE_THE_BLACK_THRONE,
            # Dream-Eaters
            ScenarioType.DARK_SIDE_OF_THE_MOON,
            ScenarioType.POINT_OF_NO_RETURN,
            ScenarioType.WEAVER_OF_THE_COSMOS,
            # Innsmouth Conspiracy
            ScenarioType.HORROR_IN_HIGH_GEAR,
            ScenarioType.INTO_THE_MAELSTROM,
            # Edge of the Earth
            ScenarioType.ICE_AND_DEATH,
            ScenarioType.THE_HEART_OF_MADNESS,
            # Scarlet Keys
            ScenarioType.DEALING_IN_THE_DARK,
            ScenarioType.CONGRESS_OF_THE_KEYS,
            # Feast of Hemlock Vale
            # Drowned City
            ScenarioType.OBSIDIAN_CANYONS,
            ScenarioType.SEPULCHRE_OF_THE_SLEEPERS,
        ],
    },
    "striking_fear": {
        "name": "Striking Fear",
        "icon": "striking_fear",
        "scenarios": [
            # Night of the Zealot
            ScenarioType.THE_GATHERING,
            ScenarioType.THE_DEVOURER_BELOW,
            # Dunwich Legacy
            ScenarioType.THE_HOUSE_ALWAYS_WINS,
            ScenarioType.THE_ESSEX_COUNTRY_EXPRESS,
            ScenarioType.UNDIMENSIONED_AND_UNSEEN,
            ScenarioType.WHERE_DOOM_AWAITS,
            # Path to Carcosa
            ScenarioType.CURTAIN_CALLS,
            ScenarioType.DIM_CARCOSA,
            # Forgotten Age
            ScenarioType.THE_CITY_OF_ARCHIVES,
            # Circle Undone
            ScenarioType.THE_WITCHING_HOUR,
            ScenarioType.IN_THE_CLUTCHES_OF_CHAOS,
            # Dream-Eaters
            ScenarioType.WAKING_NIGHTMARE,
            ScenarioType.POINT_OF_NO_RETURN,
            # Innsmouth Conspiracy
            ScenarioType.A_LIGHT_IN_THE_FOG,
            # Edge of the Earth
            ScenarioType.THE_HEART_OF_MADNESS,
            # Scarlet Keys
            ScenarioType.DEAD_HEAT,
            ScenarioType.SHADES_OF_SUFFERING,
            ScenarioType.CONGRESS_OF_THE_KEYS,
            # Hemlock Vale
            ScenarioType.THE_LONGEST_NIGHT,
            ScenarioType.THE_SILENT_HEALTH,
            # Drowned City
            ScenarioType.ONE_LAST_JOB,
            ScenarioType.THE_APIARY,
            ScenarioType.OBSIDIAN_CANYONS,
            ScenarioType.SEPULCHRE_OF_THE_SLEEPERS,
        ],
    },
    "chilling_cold": {
        "name": "Chilling Cold",
        "icon": "chilling_cold",
        "scenarios": [
            ScenarioType.THE_GATHERING,
            ScenarioType.THE_PALLID_MASK,
            ScenarioType.THE_MISKATONIC_MUSEUM,
            ScenarioType.WHERE_DOOM_AWAITS,
            ScenarioType.THE_PALLID_MASK,
            ScenarioType.THE_DOOM_OF_EZTLI,
            ScenarioType.THE_CITY_OF_ARCHIVES,
            ScenarioType.TURN_BACK_TIME,
            ScenarioType.DISAPPEARANCE_AT_THE_TWLIGHT_ESTATE,
            ScenarioType.AT_DEATHS_DOORSTEP,
            ScenarioType.UNION_AND_DISILLUSION,
            ScenarioType.BEYOND_THE_GATE_OF_SLEEP,
            ScenarioType.A_THOUSAND_SHAPES_OF_HORROR,
            ScenarioType.WEAVER_OF_THE_COSMOS,
            ScenarioType.THE_VANISHING_OF_ELINA_HARPER,
            ScenarioType.FATAL_MIRAGE,
            ScenarioType.CITY_OF_THE_ELDER_THINGS,
            ScenarioType.THE_HEART_OF_MADNESS,
            ScenarioType.RIDDLE_AND_RAIN,
            ScenarioType.ON_THIN_ICE,
            ScenarioType.WRITTEN_IN_ROCK,
            ScenarioType.THE_LONGEST_NIGHT,
            ScenarioType.ONE_LAST_JOB,
            ScenarioType.OBSIDIAN_CANYONS,
        ],
    },
    "ghouls": {
        "name": "Ghouls",
        "icon": "ghouls",
        "scenarios": [
            ScenarioType.THE_GATHERING,
            ScenarioType.THE_PALLID_MASK,
            ScenarioType.THE_DEVOURER_BELOW,
            ScenarioType.A_THOUSAND_SHAPES_OF_HORROR,
            ScenarioType.POINT_OF_NO_RETURN,
            ScenarioType.DEAD_HEAT,
            ScenarioType.WRITTEN_IN_ROCK,
        ],
    },
    "rats": {
        "name": "Rats",
        "icon": "rats",
        "scenarios": [
            ScenarioType.THE_GATHERING,
            ScenarioType.THE_HOUSE_ALWAYS_WINS,
            ScenarioType.CURTAIN_CALLS,
            ScenarioType.THE_SECRET_NAME,
            ScenarioType.A_THOUSAND_SHAPES_OF_HORROR,
            ScenarioType.THE_VANISHING_OF_ELINA_HARPER,
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.ONE_LAST_JOB,
        ],
    },
    "locked_doors": {
        "name": "Locked Doors",
        "icon": "locked_doors",
        "scenarios": [
            ScenarioType.THE_MIDNIGHT_MASKS,
            ScenarioType.EXTRACURRICULAR_ACTIVITIES,
            ScenarioType.THE_MISKATONIC_MUSEUM,
            ScenarioType.ECHO_OF_THE_PAST,
            ScenarioType.THREADS_OF_FATE,
            ScenarioType.THE_CITY_OF_ARCHIVES,
            ScenarioType.FOR_THE_GREATER_GOOD,
            ScenarioType.WAKING_NIGHTMARE,
            ScenarioType.A_THOUSAND_SHAPES_OF_HORROR,
            ScenarioType.THE_VANISHING_OF_ELINA_HARPER,
            ScenarioType.THE_LAIR_OF_DAGON,
            ScenarioType.CITY_OF_THE_ELDER_THINGS,
            ScenarioType.THE_HEART_OF_MADNESS,
            ScenarioType.RIDDLE_AND_RAIN,
            ScenarioType.SANGUINE_SHADOWS,
            ScenarioType.DEALING_IN_THE_DARK,
            ScenarioType.CONGRESS_OF_THE_KEYS,
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.ONE_LAST_JOB,
        ],
    },
    "nightgaunts": {
        "name": "Nightgaunts",
        "icon": "nightgaunts",
        "scenarios": [
            ScenarioType.THE_MIDNIGHT_MASKS,
            ScenarioType.BLOOD_ON_THE_ALTAR,
            ScenarioType.THREADS_OF_FATE,
            ScenarioType.IN_THE_CLUTCHES_OF_CHAOS,
            ScenarioType.POINT_OF_NO_RETURN,
            ScenarioType.THE_VANISHING_OF_ELINA_HARPER,
            ScenarioType.SANGUINE_SHADOWS,
            ScenarioType.OBSIDIAN_CANYONS,
        ],
    },
    "pentagram": {
        "name": "Dark Cult",
        "icon": "dark_cult",
        "scenarios": [
            ScenarioType.THE_MIDNIGHT_MASKS,
            ScenarioType.THE_DEVOURER_BELOW,
            ScenarioType.ECHO_OF_THE_PAST,
            ScenarioType.BLACK_STAR_RISE,
            ScenarioType.THREADS_OF_FATE,
            ScenarioType.THE_BOUNDARY_BEYOND,
            ScenarioType.SHATTERED_AEONS,
            ScenarioType.FOR_THE_GREATER_GOOD,
            ScenarioType.BEFORE_THE_BLACK_THRONE,
            ScenarioType.WHERE_THE_GODS_DWELL,
            ScenarioType.THE_LAIR_OF_DAGON,
            ScenarioType.DEALING_IN_THE_DARK,
            ScenarioType.DOGS_OF_WAR,
            ScenarioType.THE_APIARY,
        ],
    },
    "the_gathering": {
        "name": "The Gathering",
        "icon": "the_gathering",
        "scenarios": [ScenarioType.THE_GATHERING],
    },
    "cult_of_umordoth": {
        "name": "Cult of Umôrdhoth",
        "icon": "cult_of_umordoth",
        "scenarios": [ScenarioType.THE_MIDNIGHT_MASKS, ScenarioType.THE_DEVOURER_BELOW],
    },
    "the_midnight_masks": {
        "name": "The Midnight Masks",
        "icon": "the_midnight_masks",
        "scenarios": [
            ScenarioType.THE_MIDNIGHT_MASKS,
            ScenarioType.ECHO_OF_THE_PAST,
            ScenarioType.A_PHANTOM_OF_TRUTH,
            ScenarioType.THREADS_OF_FATE,
            ScenarioType.IN_THE_CLUTCHES_OF_CHAOS,
            ScenarioType.THE_VANISHING_OF_ELINA_HARPER,
            ScenarioType.RIDDLE_AND_RAIN,
            ScenarioType.DEALING_IN_THE_DARK,
            ScenarioType.THE_LONGEST_NIGHT,
            ScenarioType.ONE_LAST_JOB,
            ScenarioType.THE_DOOM_OF_ARKHAM_PT_I,
            ScenarioType.THE_DOOM_OF_ARKHAM_PT_II,
        ],
    },
    "the_devourer_below": {
        "name": "The Devourer Below",
        "icon": "the_devourer_below",
        "scenarios": [ScenarioType.THE_DEVOURER_BELOW, ScenarioType.THE_WITCHING_HOUR],
    },
    "agents_of_yog_sothoth": {
        "name": "Agents of Yog-Sothoth",
        "icon": "agents_of_yog_sothoth",
        "scenarios": [
            ScenarioType.THE_DEVOURER_BELOW,
            ScenarioType.EXTRACURRICULAR_ACTIVITIES,
            ScenarioType.LOST_IN_TIME_AND_SPACE,
            ScenarioType.THE_CITY_OF_ARCHIVES,
        ],
    },
    "agents_of_shub_niggurath": {
        "name": "Agents of Shub-Niggurath",
        "icon": "agents_of_shub_niggurath",
        "scenarios": [ScenarioType.THE_DEVOURER_BELOW, ScenarioType.THE_WITCHING_HOUR],
    },
    "agents_of_cthulhu": {
        "name": "Agents of Cthulhu",
        "icon": "agents_of_cthulhu",
        "scenarios": [
            ScenarioType.THE_DEVOURER_BELOW,
            ScenarioType.THE_PIT_OF_DESPAIR,
            ScenarioType.THE_WESTERN_WALL,
            ScenarioType.THE_DOOM_OF_ARKHAM_PT_I,
            ScenarioType.THE_DOOM_OF_ARKHAM_PT_II,
        ],
    },
    "agents_of_hastur": {
        "name": "Agents of Hastur",
        "icon": "agents_of_hastur",
        "scenarios": [
            ScenarioType.THE_DEVOURER_BELOW,
            ScenarioType.THE_UNSPEAKABLE_OATH,
            ScenarioType.A_PHANTOM_OF_TRUTH,
            ScenarioType.DIM_CARCOSA,
        ],
    },
}
