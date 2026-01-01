"""
Campaign Factory - Creates campaign instances based on campaign type
Provides centralized campaign creation with proper chaos bag initialization
"""

from typing import Dict, Type
from .campaign import Campaign
from .night_of_the_zealot import NightOfTheZealot
from .dunwich_legacy import DunwichLegacy
from .path_to_carcosa import PathToCarcosa
from .campaign_type import CampaignType
from ..difficulty import Difficulty


# Import all campaign classes
from .forgotten_age import ForgottenAge
from .circle_undone import CircleUndone
from .dream_eaters import DreamEatersA, DreamEatersB
from .innsmouth_conspiracy import InnsmouthConspiracy
from .edge_of_the_earth import EdgeOfTheEarth
from .scarlet_keys import ScarletKeys
from .hemlock_vale import HemlockVale
from .drowned_city import DrownedCity

# Campaign registry mapping
CAMPAIGN_REGISTRY: Dict[CampaignType, Type[Campaign]] = {
    CampaignType.NIGHT_OF_THE_ZEALOT: NightOfTheZealot,
    CampaignType.THE_DUNWICH_LEGACY: DunwichLegacy,
    CampaignType.THE_PATH_TO_CARCOSA: PathToCarcosa,
    CampaignType.THE_FORGOTTEN_AGE: ForgottenAge,
    CampaignType.THE_CIRCLE_UNDONE: CircleUndone,
    CampaignType.THE_DREAM_EATER_A: DreamEatersA,
    CampaignType.THE_DREAM_EATER_B: DreamEatersB,
    CampaignType.THE_INNSMOUTH_CONSPIRACY: InnsmouthConspiracy,
    CampaignType.THE_EDGE_OF_THE_EARTH: EdgeOfTheEarth,
    CampaignType.THE_SCARLET_KEY: ScarletKeys,
    CampaignType.THE_FEAST_OF_HEMLOCK_VALE: HemlockVale,
    CampaignType.THE_DROWNED_CITY: DrownedCity,
}


class CampaignFactory:
    """Factory for creating campaign instances with proper chaos bag setup"""

    @staticmethod
    def create_campaign(
        campaign_type: CampaignType, difficulty: Difficulty
    ) -> Campaign:
        """
        Create a campaign instance with initialized chaos bag

        Args:
            campaign_type: The campaign to create
            difficulty: Difficulty level for chaos bag setup

        Returns:
            Campaign instance with properly initialized chaos bag

        Raises:
            ValueError: If campaign type is not supported
        """
        campaign_class = CAMPAIGN_REGISTRY.get(campaign_type)

        if not campaign_class:
            raise ValueError(f"Campaign {campaign_type.value} not implemented yet")

        return campaign_class(difficulty)

    @staticmethod
    def get_supported_campaigns() -> list[CampaignType]:
        """Get list of all supported campaign types"""
        return list(CAMPAIGN_REGISTRY.keys())

    @staticmethod
    def is_campaign_supported(campaign_type: CampaignType) -> bool:
        """Check if a campaign type is supported"""
        return campaign_type in CAMPAIGN_REGISTRY


def create_campaign(campaign_type: CampaignType, difficulty: Difficulty) -> Campaign:
    """Convenience function for creating campaigns"""
    return CampaignFactory.create_campaign(campaign_type, difficulty)
