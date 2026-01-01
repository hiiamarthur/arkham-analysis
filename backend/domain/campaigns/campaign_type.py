from enum import Enum


class CampaignType(Enum):
    """All Arkham Horror LCG campaigns"""

    NIGHT_OF_THE_ZEALOT = "night_of_the_zealot"
    THE_DUNWICH_LEGACY = "the_dunwich_legacy"
    THE_PATH_TO_CARCOSA = "the_path_to_carcosa"
    THE_FORGOTTEN_AGE = "the_forgotten_age"
    THE_CIRCLE_UNDONE = "the_circle_undone"
    THE_DREAM_EATER_A = "the_dream_eater_a"
    THE_DREAM_EATER_B = "the_dream_eater_b"
    THE_INNSMOUTH_CONSPIRACY = "the_innsmouth_conspiracy"
    THE_EDGE_OF_THE_EARTH = "the_edge_of_the_earth"
    THE_SCARLET_KEY = "the_scarlet_key"
    THE_FEAST_OF_HEMLOCK_VALE = "the_feast_of_hemlock_vale"
    THE_DROWNED_CITY = "the_drowned_city"

    @property
    def display_name(self) -> str:
        """Human-readable campaign name"""
        name_mapping = {
            "night_of_the_zealot": "Night of the Zealot",
            "the_dunwich_legacy": "The Dunwich Legacy",
            "the_path_to_carcosa": "The Path to Carcosa",
            "the_forgotten_age": "The Forgotten Age",
            "the_circle_undone": "The Circle Undone",
            "the_dream_eater": "The Dream-Eaters",
            "the_innsmouth_conspiracy": "The Innsmouth Conspiracy",
            "the_edge_of_the_earth": "Edge of the Earth",
            "the_scarlet_key": "The Scarlet Keys",
            "the_feast_of_hemlock_vale": "The Feast of Hemlock Vale",
            "the_drowned_city": "The Drowned City",
        }
        return name_mapping.get(self.value, self.value.replace("_", " ").title())

    @classmethod
    def from_string(cls, value: str) -> "CampaignType":
        """Create from string, case-insensitive"""
        for campaign in cls:
            if campaign.value.lower() == value.lower():
                return campaign
        raise ValueError(f"Invalid campaign: {value}")

    def __str__(self) -> str:
        return self.display_name
