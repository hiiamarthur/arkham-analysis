"""
Scenario definitions and modifications for Arkham Horror LCG
"""

from enum import Enum
from typing import Dict, List, Any, Tuple
from .campaigns import CampaignType
from .difficulty import Difficulty


class ScenarioType(Enum):
    """All scenarios in Arkham Horror LCG - clean enum with just scenario codes"""

    # Night of the Zealot
    THE_GATHERING = "the_gathering"
    THE_MIDNIGHT_MASKS = "the_midnight_masks"
    THE_DEVOURER_BELOW = "the_devourer_below"

    # Dunwich Legacy
    EXTRACURRICULAR_ACTIVITIES = "extracurricular_activities"
    THE_HOUSE_ALWAYS_WINS = "the_house_always_wins"
    THE_MISKATONIC_MUSEUM = "the_miskatonic_museum"
    THE_ESSEX_COUNTRY_EXPRESS = "the_essex_country_express"
    BLOOD_ON_THE_ALTAR = "blood_on_the_altar"
    UNDIMENSIONED_AND_UNSEEN = "undimensioned_and_unseen"
    WHERE_DOOM_AWAITS = "where_doom_awaits"
    LOST_IN_TIME_AND_SPACE = "lost_in_time_and_space"

    # Path to Carcosa
    CURTAIN_CALLS = "curtain_calls"
    THE_LAST_KING = "the_last_king"
    ECHO_OF_THE_PAST = "echo_of_the_past"
    THE_UNSPEAKABLE_OATH = "the_unspeakable_oath"
    A_PHANTOM_OF_TRUTH = "a_phantom_of_truth"
    THE_PALLID_MASK = "the_pallid_mask"
    BLACK_STAR_RISE = "black_star_rise"
    DIM_CARCOSA = "dim_carcosa"

    # Forgotten Age
    THE_UNTAMED_WILDS = "the_untamed_wilds"
    THE_DOOM_OF_EZTLI = "the_doom_of_eztli"
    THREADS_OF_FATE = "threads_of_fate"
    THE_BOUNDARY_BEYOND = "the_boundary_beyond"
    HEART_OF_THE_ELDERS = "heart_of_the_elders"
    THE_CITY_OF_ARCHIVES = "the_city_of_archives"
    THE_DEPTHS_OF_YOTH = "the_depths_of_yoth"
    SHATTERED_AEONS = "shattered_aeons"
    TURN_BACK_TIME = "turn_back_time"

    # Circle Undone
    DISAPPEARANCE_AT_THE_TWLIGHT_ESTATE = "disappearance_at_the_twilight_estate"
    THE_WITCHING_HOUR = "the_witching_hour"
    AT_DEATHS_DOORSTEP = "at_deaths_doorstep"
    THE_SECRET_NAME = "the_secret_name"
    THE_WAGE_OF_SIN = "the_wage_of_sin"
    FOR_THE_GREATER_GOOD = "for_the_greater_good"
    UNION_AND_DISILLUSION = "union_and_disillusion"
    IN_THE_CLUTCHES_OF_CHAOS = "in_the_clutches_of_chaos"
    BEFORE_THE_BLACK_THRONE = "before_the_black_throne"

    # Dream-Eaters
    BEYOND_THE_GATE_OF_SLEEP = "beyond_the_gate_of_sleep"
    WAKING_NIGHTMARE = "waking_nightmare"
    THE_SEARCH_FOR_KADATH = "the_search_for_kadath"
    A_THOUSAND_SHAPES_OF_HORROR = "a_thousand_shapes_of_horror"
    DARK_SIDE_OF_THE_MOON = "dark_side_of_the_moon"
    POINT_OF_NO_RETURN = "point_of_no_return"
    WHERE_THE_GODS_DWELL = "where_the_gods_dwell"
    WEAVER_OF_THE_COSMOS = "weaver_of_the_cosmos"

    # Innsmouth Conspiracy
    THE_PIT_OF_DESPAIR = "the_pit_of_despair"
    THE_VANISHING_OF_ELINA_HARPER = "the_vanishing_of_elina_harper"
    IN_TOO_DEEP = "in_too_deep"
    DEVIL_REEF = "devil_reef"
    HORROR_IN_HIGH_GEAR = "horror_in_high_gear"
    A_LIGHT_IN_THE_FOG = "a_light_in_the_fog"
    THE_LAIR_OF_DAGON = "the_lair_of_dagon"
    INTO_THE_MAELSTROM = "into_the_maelstrom"

    # Edge of the Earth
    ICE_AND_DEATH = "ice_and_death"
    FATAL_MIRAGE = "fatal_mirage"
    TO_THE_FORBIDDEN_PEAKS = "to_the_forbidden_peaks"
    CITY_OF_THE_ELDER_THINGS = "city_of_the_elder_things"
    THE_HEART_OF_MADNESS = "the_heart_of_madness"

    # Scarlet Key
    RIDDLE_AND_RAIN = "riddle_and_rain"
    DEAD_HEAT = "dead_heat"
    SANGUINE_SHADOWS = "sanguine_shadows"
    DEALING_IN_THE_DARK = "dealing_in_the_dark"
    DANCING_MAD = "dancing_mad"
    ON_THIN_ICE = "on_thin_ice"
    DOGS_OF_WAR = "dogs_of_war"
    SHADES_OF_SUFFERING = "shades_of_suffering"
    WITHOUT_A_TRACE = "without_a_trace"
    CONGRESS_OF_THE_KEYS = "congress_of_the_keys"

    # Feast of Hemlock Vale

    WRITTEN_IN_ROCK = "written_in_rock"
    HEMLOCK_HOUSE = "hemlock_house"
    THE_SILENT_HEALTH = "the_silent_health"
    THE_LOST_SISTER = "the_lost_sister"
    THE_THING_IN_THE_DEPTHS = "the_thing_in_the_depths"
    THE_TWISTED_HOLLOW = "the_twisted_hollow"
    THE_LONGEST_NIGHT = "the_longest_night"
    FATE_OF_THE_VALE = "fate_of_the_vale"

    # Drowned City
    ONE_LAST_JOB = "one_last_job"
    THE_WESTERN_WALL = "the_western_wall"
    THE_DROWNED_QUARTER = "the_drowned_quarter"
    THE_APIARY = "the_apiary"
    THE_GRAND_VAULT = "the_grand_vault"
    COURT_OF_THE_ANCIENTS = "court_of_the_ancients"
    OBSIDIAN_CANYONS = "obsidian_canyons"
    SEPULCHRE_OF_THE_SLEEPERS = "sepulchre_of_the_sleepers"
    THE_DOOM_OF_ARKHAM_PT_I = "the_doom_of_arkham_pt_i"
    THE_DOOM_OF_ARKHAM_PT_II = "the_doom_of_arkham_pt_ii"

    @property
    def display_name(self) -> str:
        return NAME_TO_SCENARIO_MAP[self]

    def __str__(self) -> str:
        return self.display_name


# Separate mapping for scenario-campaign relationships
SCENARIO_CAMPAIGN_MAP: Dict[ScenarioType, CampaignType] = {
    # Night of the Zealot
    ScenarioType.THE_GATHERING: CampaignType.NIGHT_OF_THE_ZEALOT,
    ScenarioType.THE_MIDNIGHT_MASKS: CampaignType.NIGHT_OF_THE_ZEALOT,
    ScenarioType.THE_DEVOURER_BELOW: CampaignType.NIGHT_OF_THE_ZEALOT,
    # Dunwich Legacy
    ScenarioType.EXTRACURRICULAR_ACTIVITIES: CampaignType.THE_DUNWICH_LEGACY,
    ScenarioType.THE_HOUSE_ALWAYS_WINS: CampaignType.THE_DUNWICH_LEGACY,
    ScenarioType.THE_MISKATONIC_MUSEUM: CampaignType.THE_DUNWICH_LEGACY,
    ScenarioType.THE_ESSEX_COUNTRY_EXPRESS: CampaignType.THE_DUNWICH_LEGACY,
    ScenarioType.BLOOD_ON_THE_ALTAR: CampaignType.THE_DUNWICH_LEGACY,
    ScenarioType.UNDIMENSIONED_AND_UNSEEN: CampaignType.THE_DUNWICH_LEGACY,
    ScenarioType.WHERE_DOOM_AWAITS: CampaignType.THE_DUNWICH_LEGACY,
    ScenarioType.LOST_IN_TIME_AND_SPACE: CampaignType.THE_DUNWICH_LEGACY,
    # Path to Carcosa
    ScenarioType.CURTAIN_CALLS: CampaignType.THE_PATH_TO_CARCOSA,
    ScenarioType.THE_LAST_KING: CampaignType.THE_PATH_TO_CARCOSA,
    ScenarioType.ECHO_OF_THE_PAST: CampaignType.THE_PATH_TO_CARCOSA,
    ScenarioType.THE_UNSPEAKABLE_OATH: CampaignType.THE_PATH_TO_CARCOSA,
    ScenarioType.A_PHANTOM_OF_TRUTH: CampaignType.THE_PATH_TO_CARCOSA,
    ScenarioType.THE_PALLID_MASK: CampaignType.THE_PATH_TO_CARCOSA,
    ScenarioType.BLACK_STAR_RISE: CampaignType.THE_PATH_TO_CARCOSA,
    ScenarioType.DIM_CARCOSA: CampaignType.THE_PATH_TO_CARCOSA,
    # Forgotten Age
    ScenarioType.THE_UNTAMED_WILDS: CampaignType.THE_FORGOTTEN_AGE,
    ScenarioType.THE_DOOM_OF_EZTLI: CampaignType.THE_FORGOTTEN_AGE,
    ScenarioType.THREADS_OF_FATE: CampaignType.THE_FORGOTTEN_AGE,
    ScenarioType.THE_BOUNDARY_BEYOND: CampaignType.THE_FORGOTTEN_AGE,
    ScenarioType.HEART_OF_THE_ELDERS: CampaignType.THE_FORGOTTEN_AGE,
    ScenarioType.THE_CITY_OF_ARCHIVES: CampaignType.THE_FORGOTTEN_AGE,
    ScenarioType.THE_DEPTHS_OF_YOTH: CampaignType.THE_FORGOTTEN_AGE,
    ScenarioType.SHATTERED_AEONS: CampaignType.THE_FORGOTTEN_AGE,
    # Circle Undone
    ScenarioType.THE_WITCHING_HOUR: CampaignType.THE_CIRCLE_UNDONE,
    ScenarioType.AT_DEATHS_DOORSTEP: CampaignType.THE_CIRCLE_UNDONE,
    ScenarioType.THE_SECRET_NAME: CampaignType.THE_CIRCLE_UNDONE,
    ScenarioType.THE_WAGE_OF_SIN: CampaignType.THE_CIRCLE_UNDONE,
    ScenarioType.FOR_THE_GREATER_GOOD: CampaignType.THE_CIRCLE_UNDONE,
    ScenarioType.UNION_AND_DISILLUSION: CampaignType.THE_CIRCLE_UNDONE,
    ScenarioType.IN_THE_CLUTCHES_OF_CHAOS: CampaignType.THE_CIRCLE_UNDONE,
    ScenarioType.BEFORE_THE_BLACK_THRONE: CampaignType.THE_CIRCLE_UNDONE,
    # Dream-Eaters
    ScenarioType.BEYOND_THE_GATE_OF_SLEEP: CampaignType.THE_DREAM_EATER,
    ScenarioType.WAKING_NIGHTMARE: CampaignType.THE_DREAM_EATER,
    ScenarioType.THE_SEARCH_FOR_KADATH: CampaignType.THE_DREAM_EATER,
    ScenarioType.A_THOUSAND_SHAPES_OF_HORROR: CampaignType.THE_DREAM_EATER,
    ScenarioType.DARK_SIDE_OF_THE_MOON: CampaignType.THE_DREAM_EATER,
    ScenarioType.POINT_OF_NO_RETURN: CampaignType.THE_DREAM_EATER,
    ScenarioType.WHERE_THE_GODS_DWELL: CampaignType.THE_DREAM_EATER,
    ScenarioType.WEAVER_OF_THE_COSMOS: CampaignType.THE_DREAM_EATER,
    # Innsmouth Conspiracy
    ScenarioType.THE_PIT_OF_DESPAIR: CampaignType.THE_INNSMOUTH_CONSPIRACY,
    ScenarioType.THE_VANISHING_OF_ELINA_HARPER: CampaignType.THE_INNSMOUTH_CONSPIRACY,
    ScenarioType.IN_TOO_DEEP: CampaignType.THE_INNSMOUTH_CONSPIRACY,
    ScenarioType.DEVIL_REEF: CampaignType.THE_INNSMOUTH_CONSPIRACY,
    ScenarioType.HORROR_IN_HIGH_GEAR: CampaignType.THE_INNSMOUTH_CONSPIRACY,
    ScenarioType.A_LIGHT_IN_THE_FOG: CampaignType.THE_INNSMOUTH_CONSPIRACY,
    ScenarioType.THE_LAIR_OF_DAGON: CampaignType.THE_INNSMOUTH_CONSPIRACY,
    ScenarioType.INTO_THE_MAELSTROM: CampaignType.THE_INNSMOUTH_CONSPIRACY,
    # Edge of the Earth
    ScenarioType.ICE_AND_DEATH: CampaignType.THE_EDGE_OF_THE_EARTH,
    ScenarioType.FATAL_MIRAGE: CampaignType.THE_EDGE_OF_THE_EARTH,
    ScenarioType.TO_THE_FORBIDDEN_PEAKS: CampaignType.THE_EDGE_OF_THE_EARTH,
    ScenarioType.CITY_OF_THE_ELDER_THINGS: CampaignType.THE_EDGE_OF_THE_EARTH,
    ScenarioType.THE_HEART_OF_MADNESS: CampaignType.THE_EDGE_OF_THE_EARTH,
    # Scarlet Key
    ScenarioType.RIDDLE_AND_RAIN: CampaignType.THE_SCARLET_KEY,
    ScenarioType.DEAD_HEAT: CampaignType.THE_SCARLET_KEY,
    ScenarioType.SANGUINE_SHADOWS: CampaignType.THE_SCARLET_KEY,
    ScenarioType.DEALING_IN_THE_DARK: CampaignType.THE_SCARLET_KEY,
    ScenarioType.DANCING_MAD: CampaignType.THE_SCARLET_KEY,
    ScenarioType.ON_THIN_ICE: CampaignType.THE_SCARLET_KEY,
    ScenarioType.DOGS_OF_WAR: CampaignType.THE_SCARLET_KEY,
    ScenarioType.SHADES_OF_SUFFERING: CampaignType.THE_SCARLET_KEY,
    ScenarioType.WITHOUT_A_TRACE: CampaignType.THE_SCARLET_KEY,
    ScenarioType.CONGRESS_OF_THE_KEYS: CampaignType.THE_SCARLET_KEY,
    # Feast of Hemlock Vale
    ScenarioType.WRITTEN_IN_ROCK: CampaignType.THE_FEAST_OF_HEMLOCK_VALE,
    ScenarioType.HEMLOCK_HOUSE: CampaignType.THE_FEAST_OF_HEMLOCK_VALE,
    ScenarioType.THE_SILENT_HEALTH: CampaignType.THE_FEAST_OF_HEMLOCK_VALE,
    ScenarioType.THE_LOST_SISTER: CampaignType.THE_FEAST_OF_HEMLOCK_VALE,
    ScenarioType.THE_THING_IN_THE_DEPTHS: CampaignType.THE_FEAST_OF_HEMLOCK_VALE,
    ScenarioType.THE_TWISTED_HOLLOW: CampaignType.THE_FEAST_OF_HEMLOCK_VALE,
    ScenarioType.THE_LONGEST_NIGHT: CampaignType.THE_FEAST_OF_HEMLOCK_VALE,
    ScenarioType.FATE_OF_THE_VALE: CampaignType.THE_FEAST_OF_HEMLOCK_VALE,
    # Drowned City
    ScenarioType.ONE_LAST_JOB: CampaignType.THE_DROWNED_CITY,
    ScenarioType.THE_WESTERN_WALL: CampaignType.THE_DROWNED_CITY,
    ScenarioType.THE_DROWNED_QUARTER: CampaignType.THE_DROWNED_CITY,
    ScenarioType.THE_APIARY: CampaignType.THE_DROWNED_CITY,
    ScenarioType.THE_GRAND_VAULT: CampaignType.THE_DROWNED_CITY,
    ScenarioType.COURT_OF_THE_ANCIENTS: CampaignType.THE_DROWNED_CITY,
    ScenarioType.OBSIDIAN_CANYONS: CampaignType.THE_DROWNED_CITY,
    ScenarioType.SEPULCHRE_OF_THE_SLEEPERS: CampaignType.THE_DROWNED_CITY,
    ScenarioType.THE_DOOM_OF_ARKHAM_PT_I: CampaignType.THE_DROWNED_CITY,
    ScenarioType.THE_DOOM_OF_ARKHAM_PT_II: CampaignType.THE_DROWNED_CITY,
}

NAME_TO_SCENARIO_MAP: Dict[ScenarioType, str] = {
    ScenarioType.THE_GATHERING: "The Gathering",
    ScenarioType.THE_MIDNIGHT_MASKS: "The Midnight Masks",
    ScenarioType.THE_DEVOURER_BELOW: "The Devourer Below",
    ScenarioType.EXTRACURRICULAR_ACTIVITIES: "Extracurricular Activities",
    ScenarioType.THE_HOUSE_ALWAYS_WINS: "The House Always Wins",
    ScenarioType.THE_MISKATONIC_MUSEUM: "The Miskatonic Museum",
    ScenarioType.THE_ESSEX_COUNTRY_EXPRESS: "The Essex Country Express",
    ScenarioType.BLOOD_ON_THE_ALTAR: "Blood on the Altar",
    ScenarioType.UNDIMENSIONED_AND_UNSEEN: "Undimensioned and Unseen",
    ScenarioType.WHERE_DOOM_AWAITS: "Where Doom Awaits",
    ScenarioType.LOST_IN_TIME_AND_SPACE: "Lost in Time and Space",
    ScenarioType.CURTAIN_CALLS: "Curtain Calls",
    ScenarioType.THE_LAST_KING: "The Last King",
    ScenarioType.ECHO_OF_THE_PAST: "Echo of the Past",
    ScenarioType.THE_UNSPEAKABLE_OATH: "The Unspeakable Oath",
    ScenarioType.A_PHANTOM_OF_TRUTH: "A Phantom of Truth",
    ScenarioType.THE_PALLID_MASK: "The Pallid Mask",
    ScenarioType.BLACK_STAR_RISE: "Black Star Rise",
    ScenarioType.DIM_CARCOSA: "Dim Carcosa",
    ScenarioType.THE_UNTAMED_WILDS: "The Untamed Wilds",
    ScenarioType.THE_DOOM_OF_EZTLI: "The Doom of Eztli",
    ScenarioType.THREADS_OF_FATE: "Threads of Fate",
    ScenarioType.THE_BOUNDARY_BEYOND: "The Boundary Beyond",
    ScenarioType.HEART_OF_THE_ELDERS: "Heart of the Elders",
    ScenarioType.THE_CITY_OF_ARCHIVES: "The City of Archives",
    ScenarioType.THE_DEPTHS_OF_YOTH: "The Depths of Yoth",
    ScenarioType.SHATTERED_AEONS: "Shattered Aeons",
    ScenarioType.TURN_BACK_TIME: "Turn Back Time",
    ScenarioType.THE_WITCHING_HOUR: "The Witching Hour",
    ScenarioType.AT_DEATHS_DOORSTEP: "At Death's Doorstep",
    ScenarioType.THE_SECRET_NAME: "The Secret Name",
    ScenarioType.THE_WAGE_OF_SIN: "The Wage of Sin",
    ScenarioType.FOR_THE_GREATER_GOOD: "For the Greater Good",
    ScenarioType.UNION_AND_DISILLUSION: "Union and Disillusion",
    ScenarioType.IN_THE_CLUTCHES_OF_CHAOS: "In the Clutches of Chaos",
    ScenarioType.BEFORE_THE_BLACK_THRONE: "Before the Black Throne",
    ScenarioType.BEYOND_THE_GATE_OF_SLEEP: "Beyond the Gate of Sleep",
    ScenarioType.WAKING_NIGHTMARE: "Waking Nightmare",
    ScenarioType.THE_SEARCH_FOR_KADATH: "The Search for Kadath",
    ScenarioType.A_THOUSAND_SHAPES_OF_HORROR: "A Thousand Shapes of Horror",
    ScenarioType.DARK_SIDE_OF_THE_MOON: "Dark Side of the Moon",
    ScenarioType.POINT_OF_NO_RETURN: "Point of No Return",
    ScenarioType.WHERE_THE_GODS_DWELL: "Where the Gods Dwell",
    ScenarioType.WEAVER_OF_THE_COSMOS: "Weaver of the Cosmos",
    ScenarioType.THE_PIT_OF_DESPAIR: "The Pit of Despair",
    ScenarioType.THE_VANISHING_OF_ELINA_HARPER: "The Vanishing of Elina Harper",
    ScenarioType.IN_TOO_DEEP: "In Too Deep",
    ScenarioType.DEVIL_REEF: "Devil Reef",
    ScenarioType.HORROR_IN_HIGH_GEAR: "Horror in High Gear",
    ScenarioType.A_LIGHT_IN_THE_FOG: "A Light in the Fog",
    ScenarioType.THE_LAIR_OF_DAGON: "The Lair of Dagon",
    ScenarioType.INTO_THE_MAELSTROM: "Into the Maelstrom",
    ScenarioType.ICE_AND_DEATH: "Ice and Death",
    ScenarioType.FATAL_MIRAGE: "Fatal Mirage",
    ScenarioType.TO_THE_FORBIDDEN_PEAKS: "To the Forbidden Peaks",
    ScenarioType.CITY_OF_THE_ELDER_THINGS: "City of the Elder Things",
    ScenarioType.THE_HEART_OF_MADNESS: "The Heart of Madness",
    ScenarioType.RIDDLE_AND_RAIN: "Riddle and Rain",
    ScenarioType.DEAD_HEAT: "Dead Heat",
    ScenarioType.SANGUINE_SHADOWS: "Sanguine Shadows",
    ScenarioType.DEALING_IN_THE_DARK: "Dealing in the Dark",
    ScenarioType.DANCING_MAD: "Dancing Mad",
    ScenarioType.ON_THIN_ICE: "On Thin Ice",
    ScenarioType.DOGS_OF_WAR: "Dogs of War",
    ScenarioType.SHADES_OF_SUFFERING: "Shades of Suffering",
    ScenarioType.WITHOUT_A_TRACE: "Without a Trace",
    ScenarioType.CONGRESS_OF_THE_KEYS: "Congress of the Keys",
    ScenarioType.WRITTEN_IN_ROCK: "Written in Rock",
    ScenarioType.HEMLOCK_HOUSE: "Hemlock House",
    ScenarioType.THE_SILENT_HEALTH: "The Silent Health",
    ScenarioType.THE_LOST_SISTER: "The Lost Sister",
    ScenarioType.THE_THING_IN_THE_DEPTHS: "The Thing in the Depths",
    ScenarioType.THE_TWISTED_HOLLOW: "The Twisted Hollow",
    ScenarioType.THE_LONGEST_NIGHT: "The Longest Night",
    ScenarioType.FATE_OF_THE_VALE: "Fate of the Vale",
    ScenarioType.ONE_LAST_JOB: "One Last Job",
    ScenarioType.THE_WESTERN_WALL: "The Western Wall",
    ScenarioType.THE_DROWNED_QUARTER: "The Drowned Quarter",
    ScenarioType.THE_APIARY: "The Apiary",
    ScenarioType.THE_GRAND_VAULT: "The Grand Vault",
    ScenarioType.COURT_OF_THE_ANCIENTS: "Court of the Ancients",
    ScenarioType.OBSIDIAN_CANYONS: "Obsidian Canyons",
    ScenarioType.SEPULCHRE_OF_THE_SLEEPERS: "Sepulchre of the Sleepers",
    ScenarioType.THE_DOOM_OF_ARKHAM_PT_I: "The Doom of Arkham Pt I",
    ScenarioType.THE_DOOM_OF_ARKHAM_PT_II: "The Doom of Arkham Pt II",
}


# Utility functions for working with scenarios
def get_scenario_campaign(scenario: ScenarioType) -> CampaignType:
    """Get the campaign this scenario belongs to"""
    return SCENARIO_CAMPAIGN_MAP[scenario]


def get_scenarios_by_campaign(campaign: CampaignType) -> List[ScenarioType]:
    """Get all scenarios for a campaign"""
    return [
        scenario
        for scenario, scen_campaign in SCENARIO_CAMPAIGN_MAP.items()
        if scen_campaign == campaign
    ]


def get_scenario_display_name(scenario: ScenarioType) -> str:
    """Human-readable scenario name"""
    return scenario.value.replace("_", " ").title()


# Scenario-specific chaos token modifications
SCENARIO_MODIFICATIONS: Dict[
    ScenarioType, Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]
] = {
    ScenarioType.THE_GATHERING: {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of Ghoul enemies at your location.",
                "value": "X",
            },
            ("hard", "expert"): {
                "effect": "-2. If you fail, after this skill test, search the encounter deck and discard pile for a Ghoul enemy, and draw it. Shuffle the encounter deck.",
                "value": "2",
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
                "effect": "-4. If there is a Ghoul enemy at your location, take 1 damage and 1 horror. If you fail, take 2 horror.",
                "value": -4,
            },
        },
    },
    ScenarioType.THE_MIDNIGHT_MASKS: {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the highest number of doom on a Cultist enemy in play.",
                "value": "-X",
            },
            ("hard", "expert"): {
                "effect": "-X. X is the total number of doom in play.",
                "value": "-X",
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
    # Add more scenario modifications as needed...
}


def get_scenario_modifications(
    scenario: ScenarioType, difficulty: Difficulty
) -> Dict[str, Dict[str, Any]]:
    """
    Get token modifications for a specific scenario and difficulty

    Returns:
        Dict with token types as keys and modification data as values
    """
    scenario_data = SCENARIO_MODIFICATIONS.get(scenario, {})
    result = {}

    for token, difficulty_data in scenario_data.items():
        for difficulty_tuple, token_data in difficulty_data.items():
            if difficulty.value in difficulty_tuple:
                result[token] = token_data
                break

    return result


def get_scenario_count(campaign: CampaignType) -> int:
    """Get number of scenarios in a campaign"""
    return len(get_scenarios_by_campaign(campaign))
