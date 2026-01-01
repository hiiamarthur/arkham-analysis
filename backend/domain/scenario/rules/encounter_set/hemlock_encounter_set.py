from domain import ScenarioType

HEMLOCK_ENCOUNTER_SET = {
    # Feast of Hemlock Vale Encounter Sets
    "the_first_day": {
        "name": "The First Day",
        "icon": "the_first_day",
        "scenarios": [
            ScenarioType.WRITTEN_IN_ROCK,
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.THE_THING_IN_THE_DEPTHS,
            ScenarioType.THE_TWISTED_HOLLOW,
        ],
    },
    "the_second_day": {
        "name": "The Second Day",
        "icon": "the_second_day",
        "scenarios": [
            ScenarioType.WRITTEN_IN_ROCK,
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.THE_THING_IN_THE_DEPTHS,
        ],
    },
    "the_final_day": {
        "name": "The Final Day",
        "icon": "the_final_day",
        "scenarios": [
            ScenarioType.WRITTEN_IN_ROCK,
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.THE_THING_IN_THE_DEPTHS,
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "residents": {
        "name": "Residents",
        "icon": "residents",
        "scenarios": [
            ScenarioType.WRITTEN_IN_ROCK,
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.THE_LONGEST_NIGHT,
        ],
    },
    "horrors_in_the_rock": {
        "name": "Horrors in the Rock",
        "icon": "horrors_in_the_rock",
        "scenarios": [
            ScenarioType.WRITTEN_IN_ROCK,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "refractions": {
        "name": "Refractions",
        "icon": "refractions",
        "scenarios": [
            ScenarioType.WRITTEN_IN_ROCK,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "agents_of_the_colour": {
        "name": "Agents of the Colour",
        "icon": "agents_of_the_colour",
        "scenarios": [
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "blight": {
        "name": "Blight",
        "icon": "blight",
        "scenarios": [
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.THE_THING_IN_THE_DEPTHS,
            ScenarioType.THE_LONGEST_NIGHT,
        ],
    },
    "fire": {
        "name": "Fire",
        "icon": "fire",
        "scenarios": [
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_LONGEST_NIGHT,
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "transfiguration": {
        "name": "Transfiguration",
        "icon": "transfiguration",
        "scenarios": [
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.THE_LONGEST_NIGHT,
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "mutations": {
        "name": "Mutations",
        "icon": "mutations",
        "scenarios": [
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.THE_THING_IN_THE_DEPTHS,
        ],
    },
    "myconids": {
        "name": "Myconids",
        "icon": "myconids",
        "scenarios": [
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.THE_TWISTED_HOLLOW,
        ],
    },
    "the_forest": {
        "name": "The Forest",
        "icon": "the_forest",
        "scenarios": [
            ScenarioType.THE_THING_IN_THE_DEPTHS,
            ScenarioType.THE_TWISTED_HOLLOW,
        ],
    },
    "day_of_the_feast": {
        "name": "Day of the Feast",
        "icon": "day_of_the_feast",
        "scenarios": [
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "creatures_of_the_vale": {
        "name": "Creatures of the Vale",
        "icon": "creatures_of_the_vale",
        "scenarios": [
            ScenarioType.WRITTEN_IN_ROCK,
            ScenarioType.THE_THING_IN_THE_DEPTHS,
            ScenarioType.THE_TWISTED_HOLLOW,
            ScenarioType.THE_LONGEST_NIGHT,
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "hemlock_poison": {
        "name": "Hemlock Poison",
        "icon": "hemlock_poison",
        "scenarios": [
            ScenarioType.HEMLOCK_HOUSE,
            ScenarioType.THE_SILENT_HEATH,
            ScenarioType.THE_LOST_SISTER,
            ScenarioType.THE_THING_IN_THE_DEPTHS,
            ScenarioType.THE_TWISTED_HOLLOW,
            ScenarioType.FATE_OF_THE_VALE,
        ],
    },
    "day_of_rest": {
        "name": "Day of Rest",
        "icon": "day_of_rest",
        "scenarios": [],
    },
    "the_vale": {
        "name": "The Vale",
        "icon": "the_vale",
        "scenarios": [ScenarioType.FATE_OF_THE_VALE],
    },
    "written_in_rock": {
        "name": "Written in Rock",
        "icon": "written_in_rock",
        "scenarios": [ScenarioType.WRITTEN_IN_ROCK],
    },
    "hemlock_house": {
        "name": "Hemlock House",
        "icon": "hemlock_house",
        "scenarios": [ScenarioType.HEMLOCK_HOUSE],
    },
    "the_silent_heath": {
        "name": "The Silent Heath",
        "icon": "the_silent_heath",
        "scenarios": [ScenarioType.THE_SILENT_HEATH],
    },
    "the_lost_sister": {
        "name": "The Lost Sister",
        "icon": "the_lost_sister",
        "scenarios": [ScenarioType.THE_LOST_SISTER],
    },
    "the_thing_in_the_depths": {
        "name": "The Thing in the Depths",
        "icon": "the_thing_in_the_depths",
        "scenarios": [ScenarioType.THE_THING_IN_THE_DEPTHS],
    },
    "the_twisted_hollow": {
        "name": "The Twisted Hollow",
        "icon": "the_twisted_hollow",
        "scenarios": [ScenarioType.THE_TWISTED_HOLLOW],
    },
    "the_longest_night": {
        "name": "The Longest Night",
        "icon": "the_longest_night",
        "scenarios": [ScenarioType.THE_LONGEST_NIGHT],
    },
    "fate_of_the_vale": {
        "name": "Fate of the Vale",
        "icon": "fate_of_the_vale",
        "scenarios": [ScenarioType.FATE_OF_THE_VALE],
    },
}
