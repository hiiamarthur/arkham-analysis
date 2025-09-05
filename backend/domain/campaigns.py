"""
Campaign definitions for Arkham Horror LCG
"""

from enum import Enum
from typing import Dict, List


class CampaignType(Enum):
    """All Arkham Horror LCG campaigns"""
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
            "the_drowned_city": "The Drowned City"
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


class CycleType(Enum):
    """Campaign cycles for organization"""
    CORE = "core"
    DUNWICH = "dunwich"
    CARCOSA = "carcosa"
    FORGOTTEN = "forgotten"
    CIRCLE = "circle"
    DREAM = "dream"
    INNSMOUTH = "innsmouth"
    EDGE = "edge"
    SCARLET = "scarlet"
    HEMLOCK = "hemlock"
    DROWNED = "drowned"


# Campaign to cycle mapping
CAMPAIGN_CYCLES: Dict[CampaignType, CycleType] = {
    CampaignType.NIGHT_OF_THE_ZEALOT: CycleType.CORE,
    CampaignType.THE_DUNWICH_LEGACY: CycleType.DUNWICH,
    CampaignType.THE_PATH_TO_CARCOSA: CycleType.CARCOSA,
    CampaignType.THE_FORGOTTEN_AGE: CycleType.FORGOTTEN,
    CampaignType.THE_CIRCLE_UNDONE: CycleType.CIRCLE,
    CampaignType.THE_DREAM_EATER: CycleType.DREAM,
    CampaignType.THE_INNSMOUTH_CONSPIRACY: CycleType.INNSMOUTH,
    CampaignType.THE_EDGE_OF_THE_EARTH: CycleType.EDGE,
    CampaignType.THE_SCARLET_KEY: CycleType.SCARLET,
    CampaignType.THE_FEAST_OF_HEMLOCK_VALE: CycleType.HEMLOCK,
    CampaignType.THE_DROWNED_CITY: CycleType.DROWNED,
}


def get_campaign_cycle(campaign: CampaignType) -> CycleType:
    """Get the cycle for a campaign"""
    return CAMPAIGN_CYCLES[campaign]


def get_campaigns_in_cycle(cycle: CycleType) -> List[CampaignType]:
    """Get all campaigns in a cycle"""
    return [campaign for campaign, camp_cycle in CAMPAIGN_CYCLES.items() if camp_cycle == cycle]