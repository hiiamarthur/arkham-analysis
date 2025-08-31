from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List

from scoring_model.Token.chaos_bag import ChaosBag
from scoring_model.Token.token import (
    AutoFailToken,
    ChaosToken,
    ElderSignToken,
    MinusEightToken,
    MinusFiveToken,
    MinusFourToken,
    MinusOneToken,
    MinusTwoToken,
    MinusThreeToken,
    PlusOneToken,
    SkullToken,
    ZeroToken,
    CultistToken,
    TabletToken,
    ElderThingToken,
)


class Difficulty(Enum):
    EASY = "easy"
    STANDARD = "standard"
    HARD = "hard"
    EXPERT = "expert"


class CAMPAIGNTYPE(Enum):
    NIGHT_OF_THE_ZEALOT = "night_of_the_zealot"
    THE_DUNWICH_LEGACY = "the_dunwich_legacy"
    THE_PATH_TO_CARCOSA = "the_path_to_carcosa"
    THE_FORGOTTEN_AGE = "the_forgotten_age"
    THE_CIRCLE_UNDONE = "the_circle_undone"
    THE_DREAM_EATER = "the_dream_eater"
    THE_INNSMOUTH_CONSPIRACY = "the_innsmouth_conspiracy"
    THE_EDGE_OF_THE_EARTH = "the_edge_of_the_earth"
    THE_SCARLET_KEY = "the_scarlet_key"
    THE_FEAST_OF_HEMLOCK_VALE = "the_feast_of_hemlock_vale"
    THE_DROWNED_CITY = "the_drowned_city"


class ScenarioType(Enum):
    THE_GATHERING = (CAMPAIGNTYPE.NIGHT_OF_THE_ZEALOT, "the_gathering")
    THE_MIDNIGHT_MASKS = (CAMPAIGNTYPE.NIGHT_OF_THE_ZEALOT, "the_midnight_masks")
    THE_DEVOURER_BELOW = (CAMPAIGNTYPE.NIGHT_OF_THE_ZEALOT, "the_devourer_below")

    EXTRACURRICULAR_ACTIVITIES = (
        CAMPAIGNTYPE.THE_DUNWICH_LEGACY,
        "extracurricular_activities",
    )
    THE_HOUSE_ALWAYS_WINS = (CAMPAIGNTYPE.THE_DUNWICH_LEGACY, "the_house_always_wins")
    THE_MISKATONIC_MUSEUM = (CAMPAIGNTYPE.THE_DUNWICH_LEGACY, "the_miskatonic_museum")
    THE_ESSEX_COUNTRY_EXPRESS = (
        CAMPAIGNTYPE.THE_DUNWICH_LEGACY,
        "the_essex_country_express",
    )
    BLOOD_ON_THE_ALTAR = (CAMPAIGNTYPE.THE_DUNWICH_LEGACY, "blood_on_the_altar")
    UNDIMENSIONED_AND_UNSEEN = (
        CAMPAIGNTYPE.THE_DUNWICH_LEGACY,
        "undimensioned_and_unseen",
    )
    WHERE_DOOM_AWAITS = (CAMPAIGNTYPE.THE_DUNWICH_LEGACY, "where_doom_awaits")
    LOST_IN_TIME_AND_SPACE = (CAMPAIGNTYPE.THE_DUNWICH_LEGACY, "lost_in_time_and_space")

    CURTAIN_CALLS = (CAMPAIGNTYPE.THE_PATH_TO_CARCOSA, "curtain_calls")
    THE_LAST_KING = (CAMPAIGNTYPE.THE_PATH_TO_CARCOSA, "the_last_king")
    ECHO_OF_THE_PAST = (CAMPAIGNTYPE.THE_PATH_TO_CARCOSA, "echo_of_the_past")
    THE_UNSPEAKABLE_OATH = (CAMPAIGNTYPE.THE_PATH_TO_CARCOSA, "the_unspeakable_oath")
    A_PHANTOM_OF_TRUTH = (CAMPAIGNTYPE.THE_PATH_TO_CARCOSA, "a_phantom_of_truth")
    THE_PALLID_MASK = (CAMPAIGNTYPE.THE_PATH_TO_CARCOSA, "the_pallid_mask")
    BLACK_STAR_RISE = (CAMPAIGNTYPE.THE_PATH_TO_CARCOSA, "black_star_rise")
    DIM_CARCOSA = (CAMPAIGNTYPE.THE_PATH_TO_CARCOSA, "dim_carcosa")

    THE_UNTAMED_WILDS = (CAMPAIGNTYPE.THE_FORGOTTEN_AGE, "the_untamed_wilds")
    THE_DOOM_OF_EZTIL = (CAMPAIGNTYPE.THE_FORGOTTEN_AGE, "the_doom_of_eztli")
    THREADS_OF_FATE = (CAMPAIGNTYPE.THE_FORGOTTEN_AGE, "threads_of_fate")
    THE_BOUNDARY_BEYOND = (CAMPAIGNTYPE.THE_FORGOTTEN_AGE, "the_boundary_beyond")
    HEART_OF_THE_ELDERS = (CAMPAIGNTYPE.THE_FORGOTTEN_AGE, "heart_of_the_elders")
    THE_CITY_OF_ARCHIVES = (CAMPAIGNTYPE.THE_FORGOTTEN_AGE, "the_city_of_archives")
    THE_DEPTHS_OF_YOTH = (CAMPAIGNTYPE.THE_FORGOTTEN_AGE, "the_depths_of_yoth")
    SHATTERED_AEONS = (CAMPAIGNTYPE.THE_FORGOTTEN_AGE, "shattered_aeons")

    THE_WITCHING_HOUR = (CAMPAIGNTYPE.THE_CIRCLE_UNDONE, "the_witching_hour")
    AT_DEATHS_DOORSTEP = (CAMPAIGNTYPE.THE_CIRCLE_UNDONE, "at_deaths_doorstep")
    THE_SECRET_NAME = (CAMPAIGNTYPE.THE_CIRCLE_UNDONE, "the_secret_name")
    THE_WAGE_OF_SIN = (CAMPAIGNTYPE.THE_CIRCLE_UNDONE, "the_wage_of_sin")
    FOR_THE_GREATER_GOOD = (CAMPAIGNTYPE.THE_CIRCLE_UNDONE, "for_the_greater_good")
    UNION_AND_DISILLUSION = (CAMPAIGNTYPE.THE_CIRCLE_UNDONE, "union_and_disillusion")
    IN_THE_CLUTCHES_OF_CHAOS = (
        CAMPAIGNTYPE.THE_CIRCLE_UNDONE,
        "in_the_clutches_of_chaos",
    )
    BEFORE_THE_BLACK_THRONE = (
        CAMPAIGNTYPE.THE_CIRCLE_UNDONE,
        "before_the_black_throne",
    )

    BEYOND_THE_GATE_OF_SLEEP = (
        CAMPAIGNTYPE.THE_DREAM_EATER,
        "beyond_the_gate_of_sleep",
    )
    WAKING_NIGHTMARE = (CAMPAIGNTYPE.THE_DREAM_EATER, "waking_nightmare")
    THE_SEARCH_FOR_KADATH = (CAMPAIGNTYPE.THE_DREAM_EATER, "the_search_for_kadath")
    A_THOUSAND_SHAPES_OF_HORROR = (
        CAMPAIGNTYPE.THE_DREAM_EATER,
        "a_thousand_shapes_of_horror",
    )
    DARK_SIDE_OF_THE_MOON = (CAMPAIGNTYPE.THE_DREAM_EATER, "dark_side_of_the_moon")
    POINT_OF_NO_RETURN = (CAMPAIGNTYPE.THE_DREAM_EATER, "point_of_no_return")
    WHERE_THE_GODS_DWELL = (CAMPAIGNTYPE.THE_DREAM_EATER, "where_the_gods_dwell")
    WEAVER_OF_THE_COSMOS = (CAMPAIGNTYPE.THE_DREAM_EATER, "weaver_of_the_cosmos")

    THE_PIT_OF_DESPAIR = (CAMPAIGNTYPE.THE_INNSMOUTH_CONSPIRACY, "the_pit_of_despair")
    THE_VANISHING_OF_ELINA_HARPER = (
        CAMPAIGNTYPE.THE_INNSMOUTH_CONSPIRACY,
        "the_vanishing_of_elina_harper",
    )
    IN_TOO_DEEP = (CAMPAIGNTYPE.THE_INNSMOUTH_CONSPIRACY, "in_too_deep")
    DEVIL_REEF = (CAMPAIGNTYPE.THE_INNSMOUTH_CONSPIRACY, "devil_reef")
    HORROR_IN_HIGH_GEAR = (CAMPAIGNTYPE.THE_INNSMOUTH_CONSPIRACY, "horror_in_high_gear")
    A_LIGHT_IN_THE_FOG = (CAMPAIGNTYPE.THE_INNSMOUTH_CONSPIRACY, "a_light_in_the_fog")
    THE_LAIR_OF_DAGON = (CAMPAIGNTYPE.THE_INNSMOUTH_CONSPIRACY, "the_lair_of_dagon")
    INTO_THE_MAELSTROM = (CAMPAIGNTYPE.THE_INNSMOUTH_CONSPIRACY, "into_the_maelstrom")

    ICE_AND_DEATH = (CAMPAIGNTYPE.THE_EDGE_OF_THE_EARTH, "ice_and_death")
    FATAL_MIRAGE = (CAMPAIGNTYPE.THE_EDGE_OF_THE_EARTH, "fatal_mirage")
    TO_THE_FORBIDDEN_PEAKS = (
        CAMPAIGNTYPE.THE_EDGE_OF_THE_EARTH,
        "to_the_forbidden_peaks",
    )
    CITY_OF_THE_ELDER_THINGS = (
        CAMPAIGNTYPE.THE_EDGE_OF_THE_EARTH,
        "city_of_the_elder_things",
    )
    THE_HEART_OF_MADNESS = (CAMPAIGNTYPE.THE_EDGE_OF_THE_EARTH, "the_heart_of_madness")

    RIDDLE_AND_RAIN = (CAMPAIGNTYPE.THE_SCARLET_KEY, "riddle_and_rain")
    DEAR_HEAT = (CAMPAIGNTYPE.THE_SCARLET_KEY, "dear_heat")
    SANGUINE_SHADOWS = (CAMPAIGNTYPE.THE_SCARLET_KEY, "sanguine_shadows")
    DEALING_IN_THE_DARK = (CAMPAIGNTYPE.THE_SCARLET_KEY, "dealing_in_the_dark")
    DANCING_MAD = (CAMPAIGNTYPE.THE_SCARLET_KEY, "dancing_mad")
    ON_THE_THIN_ICE = (CAMPAIGNTYPE.THE_SCARLET_KEY, "on_the_thin_ice")
    DOGS_OF_WAR = (CAMPAIGNTYPE.THE_SCARLET_KEY, "dogs_of_war")
    SHADES_OF_SUFFERING = (CAMPAIGNTYPE.THE_SCARLET_KEY, "shades_of_suffering")
    WITHOUT_A_TRACE = (CAMPAIGNTYPE.THE_SCARLET_KEY, "without_a_trace")
    CONGRESS_OF_THE_KEYS = (CAMPAIGNTYPE.THE_SCARLET_KEY, "congress_of_the_keys")

    WRITTEN_IN_ROCK = (CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE, "written_in_rock")
    HEMLOCK_HOUSE = (CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE, "hemlock_house")
    THE_SILENT_HEALTH = (CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE, "the_silent_health")
    THE_LOST_SISTER = (CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE, "the_lost_sister")
    THE_THING_IN_THE_DEPTHS = (
        CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE,
        "the_thing_in_the_depths",
    )
    THE_TWISTED_HOLLOW = (CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE, "the_twisted_hollow")
    THE_LONGEST_NIGHT = (CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE, "the_longest_night")
    FATE_OF_THE_VALE = (CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE, "fate_of_the_vale")
    THE_VALE = (CAMPAIGNTYPE.THE_FEAST_OF_HEMLOCK_VALE, "the_vale")

    ONE_LAST_JOB = (CAMPAIGNTYPE.THE_DROWNED_CITY, "one_last_job")
    THE_WESTERN_WALL = (CAMPAIGNTYPE.THE_DROWNED_CITY, "the_western_wall")
    THE_DROWNED_QUARTER = (CAMPAIGNTYPE.THE_DROWNED_CITY, "the_drowned_quarter")
    THE_APIARY = (CAMPAIGNTYPE.THE_DROWNED_CITY, "the_apiary")
    THE_GRAND_VAULT = (CAMPAIGNTYPE.THE_DROWNED_CITY, "the_grand_vault")
    COURT_OF_THE_ANCIENTS = (CAMPAIGNTYPE.THE_DROWNED_CITY, "court_of_the_ancients")
    OBSIDIAN_CANYONS = (CAMPAIGNTYPE.THE_DROWNED_CITY, "obsidian_canyons")
    SEPULCHRE_OF_THE_SLEEPERS = (
        CAMPAIGNTYPE.THE_DROWNED_CITY,
        "sepulchre_of_the_sleepers",
    )
    THE_DOOM_OF_ARKHAM_PT_I = (CAMPAIGNTYPE.THE_DROWNED_CITY, "the_doom_of_arkham_pt_i")
    THE_DOOM_OF_ARKHAM_PT_II = (
        CAMPAIGNTYPE.THE_DROWNED_CITY,
        "the_doom_of_arkham_pt_ii",
    )


# Scenario-specific token modifications
SCENARIO_MODIFICATIONS = {
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
    ScenarioType.THE_DEVOURER_BELOW: {
        "skull": {
            ("easy", "standard"): {
                "effect": "-X. X is the number of Monster enemies in play.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-3. If you fail, after this skill test, search the encounter deck and discard pile for a Monster enemy, and draw it. Shuffle the encounter deck.",
                "value": -3,
            },
        },
        "cultist": {
            ("easy", "standard"): {
                "effect": "-2. Place 1 doom on the nearest enemy.",
                "value": -2,
            },
            ("hard", "expert"): {
                "effect": "-4. Place 2 doom on the nearest enemy.",
                "value": -4,
            },
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "-3. If there is a Monster enemy at your location, take 1 damage.",
                "value": -3,
            },
            ("hard", "expert"): {
                "effect": "-5. If there is a Monster enemy at your location, take 1 damage and 1 horror.",
                "value": -5,
            },
        },
        "elder_thing": {
            ("easy", "standard"): {
                "effect": "-5. If there is an Ancient One enemy in play, reveal another token.",
                "value": -5,
            },
            ("hard", "expert"): {
                "effect": "-7. If there is an Ancient One enemy in play, reveal another token.",
                "value": -7,
            },
        },
    },
    ScenarioType.EXTRACURRICULAR_ACTIVITIES: {
        "skull": {
            ("easy", "standard"): {"effect": "Discard a card from hand", "value": -1},
            ("hard", "expert"): {"effect": "Discard a card from hand", "value": -3},
        },
        "tablet": {
            ("easy", "standard"): {
                "effect": "Move to connecting location",
                "value": -2,
            },
            ("hard", "expert"): {"effect": "Move to connecting location", "value": -4},
        },
    },
    ScenarioType.THE_HOUSE_ALWAYS_WINS: {
        "skull": {
            ("easy", "standard"): {"effect": "Lose 2 resources", "value": -2},
            ("hard", "expert"): {"effect": "Lose 2 resources", "value": -4},
        },
        "tablet": {
            ("easy", "standard"): {"effect": "Draw encounter card", "value": -3},
            ("hard", "expert"): {"effect": "Draw encounter card", "value": -5},
        },
    },
}


def get_scenario_modifications(
    scenario: ScenarioType, difficulty: Difficulty
) -> Dict[str, Dict[str, str]]:
    scenario_data = SCENARIO_MODIFICATIONS.get(scenario, {})
    result = {}

    for token, difficulty_data in scenario_data.items():
        for difficulty_tuple, token_data in difficulty_data.items():
            if difficulty.value in difficulty_tuple:
                result[token] = token_data
                break

    return result


class Campaign(ABC):
    def __init__(self, campaign_type: CAMPAIGNTYPE, difficulty: Difficulty):
        self.campaign_type = campaign_type
        self.difficulty = difficulty
        self.chaos_bag = ChaosBag(self.get_init_tokens(difficulty))

    @abstractmethod
    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
        """Create the chaos bag tokens for this campaign at the given difficulty."""
        pass


class Scenario(ABC):
    def __init__(
        self,
        campaign: Campaign,
        scenario: ScenarioType,
        difficulty: Difficulty,
    ):
        self.campaign = campaign
        self.scenario = scenario
        self.chaos_bag = campaign.chaos_bag
        self.scenario_modifications = get_scenario_modifications(scenario, difficulty)
        self._apply_scenario_modifications()

    def _apply_scenario_modifications(self):
        """Apply scenario-specific token modifications to chaos bag"""
        modifications = self._get_scenario_modifications()
        if modifications:
            self._modify_special_tokens(modifications)

    def _get_scenario_modifications(self):
        """Override in subclasses or use mapping"""
        return SCENARIO_MODIFICATIONS.get(self.scenario, {})

    def _modify_special_tokens(self, modifications):
        """Modify special tokens with scenario-specific effects"""
        from scoring_model.Token.token import (
            SkullToken,
            CultistToken,
            TabletToken,
            ElderThingToken,
        )

        for i, token in enumerate(self.chaos_bag.tokens):
            if isinstance(token, SkullToken) and "skull" in modifications:
                skull_data = modifications["skull"]
                self.chaos_bag.tokens[i] = SkullToken(
                    skull_data.get("effect", ""), skull_data.get("value", token.value)
                )
            elif isinstance(token, CultistToken) and "cultist" in modifications:
                cultist_data = modifications["cultist"]
                self.chaos_bag.tokens[i] = CultistToken(
                    cultist_data.get("effect", ""),
                    cultist_data.get("value", token.value),
                )
            elif isinstance(token, TabletToken) and "tablet" in modifications:
                tablet_data = modifications["tablet"]
                self.chaos_bag.tokens[i] = TabletToken(
                    tablet_data.get("effect", ""), tablet_data.get("value", token.value)
                )
            elif isinstance(token, ElderThingToken) and "elder_thing" in modifications:
                elder_data = modifications["elder_thing"]
                self.chaos_bag.tokens[i] = ElderThingToken(
                    elder_data.get("effect", ""), elder_data.get("value", token.value)
                )


class NightOfTheZealot(Campaign):

    def __init__(self, difficulty: Difficulty):
        super().__init__(CAMPAIGNTYPE.NIGHT_OF_THE_ZEALOT, difficulty)

    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
        base_tokens = [
            ElderSignToken(),
            AutoFailToken(),
        ]

        token_configs = {
            Difficulty.EASY: {
                PlusOneToken: 2,
                ZeroToken: 3,
                MinusOneToken: 3,
                MinusTwoToken: 2,
            },
            Difficulty.STANDARD: {
                PlusOneToken: 1,
                ZeroToken: 2,
                MinusOneToken: 3,
                MinusTwoToken: 2,
                MinusThreeToken: 1,
                MinusFourToken: 1,
            },
            Difficulty.HARD: {
                ZeroToken: 3,
                MinusOneToken: 2,
                MinusTwoToken: 2,
                MinusThreeToken: 2,
                MinusFourToken: 1,
            },
            Difficulty.EXPERT: {
                ZeroToken: 1,
                MinusOneToken: 2,
                MinusTwoToken: 2,
                MinusThreeToken: 3,
                MinusFourToken: 4,
                MinusFiveToken: 1,
                MinusEightToken: 1,
            },
        }

        config = token_configs.get(difficulty, {})
        for token_type, count in config.items():
            if isinstance(token_type, tuple):
                token_class, *args = token_type
                base_tokens.extend([token_class(*args) for _ in range(count)])
            else:
                base_tokens.extend([token_type() for _ in range(count)])

        return base_tokens


class TheDunwichLegacy(Campaign):
    def __init__(self, difficulty: Difficulty):
        super().__init__(CAMPAIGNTYPE.THE_DUNWICH_LEGACY, difficulty)

    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
        base_tokens = [
            ElderSignToken(),
            AutoFailToken(),
        ]

        token_configs = {
            Difficulty.EASY: {
                PlusOneToken: 1,
                ZeroToken: 2,
                MinusOneToken: 2,
                MinusTwoToken: 2,
                (SkullToken, "", -1): 1,
                (SkullToken, "", -2): 1,
            },
            Difficulty.STANDARD: {
                ZeroToken: 1,
                MinusOneToken: 2,
                MinusTwoToken: 2,
                (SkullToken, "", -2): 1,
                (SkullToken, "", -3): 1,
            },
            Difficulty.HARD: {
                ZeroToken: 1,
                MinusOneToken: 1,
                MinusTwoToken: 1,
                (SkullToken, "", -3): 1,
                (SkullToken, "", -4): 1,
            },
            Difficulty.EXPERT: {
                MinusOneToken: 1,
                (SkullToken, "", -4): 1,
                (SkullToken, "", -5): 1,
            },
        }

        config = token_configs.get(difficulty, {})
        for token_type, count in config.items():
            if isinstance(token_type, tuple):
                token_class, *args = token_type
                base_tokens.extend([token_class(*args) for _ in range(count)])
            else:
                base_tokens.extend([token_type() for _ in range(count)])

        return base_tokens


# Scenario factory function
def create_scenario(
    campaign: Campaign, scenario_type: ScenarioType, difficulty: Difficulty
) -> Scenario:
    """Factory function to create scenarios with proper chaos bag modifications"""

    class DynamicScenario(Scenario):
        pass

    return DynamicScenario(campaign, scenario_type, difficulty)


# Convenience functions for specific campaigns
def create_night_of_zealot_scenario(
    difficulty: Difficulty, scenario_type: ScenarioType
) -> Scenario:
    """Create Night of the Zealot scenario"""
    campaign = NightOfTheZealot(difficulty)
    return create_scenario(campaign, scenario_type, difficulty)


def create_dunwich_scenario(
    difficulty: Difficulty, scenario_type: ScenarioType
) -> Scenario:
    """Create Dunwich Legacy scenario"""
    campaign = TheDunwichLegacy(difficulty)
    return create_scenario(campaign, scenario_type, difficulty)
