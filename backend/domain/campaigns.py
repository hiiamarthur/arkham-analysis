"""
Campaign definitions for Arkham Horror LCG
"""

from enum import Enum
from typing import Dict, List

from .campaigns import CampaignType


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
    return [
        campaign
        for campaign, camp_cycle in CAMPAIGN_CYCLES.items()
        if camp_cycle == cycle
    ]
