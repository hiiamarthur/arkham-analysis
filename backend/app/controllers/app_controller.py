from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.schemas.card_schema import Card
from app.services.app_service import AppService

logger = logging.getLogger(__name__)


class AppController:
    """Simplified controller that delegates to service layer"""

    def __init__(self, db: AsyncSession):
        self.app_service = AppService(db)

    async def fetch_cards(self, encounter: int = 0) -> None:
        """Delegate card fetching to service layer"""
        return await self.app_service.fetch_cards(encounter)

    async def get_taboos(self) -> List[Dict[str, Any]]:
        """Delegate taboo fetching to service layer"""
        return await self.app_service.get_taboos()

    async def get_card(self, card_id: str) -> Card:
        """Delegate card retrieval to service layer"""
        return await self.app_service.get_card(card_id)

    async def calculate_card_value(self, card_id: str) -> float:
        """Delegate card value calculation to service layer"""
        return await self.app_service.calculate_card_value(card_id)

    async def get_cards_by_encounter(self, encounter: int, limit: int = 100) -> List[Card]:
        """Delegate cards by encounter to service layer"""
        return await self.app_service.get_cards_by_encounter(encounter, limit)

    async def search_cards(self, query: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Delegate card search to service layer"""
        return await self.app_service.search_cards(query, page, limit)
    
    # Repository access methods for direct database access when needed
    async def get_card_repository(self):
        """Get card repository via service layer"""
        return await self.app_service.get_card_repository()
    
    async def get_taboo_repository(self):
        """Get taboo repository via service layer"""  
        return await self.app_service.get_taboo_repository()
    
    async def get_trait_repository(self):
        """Get trait repository via service layer"""
        return await self.app_service.get_trait_repository()
    
    # Service coordination methods
    async def sync_with_arkhamdb(self):
        """Sync with ArkhamDB via service layer"""
        return await self.app_service.sync_with_arkhamdb()
    
    async def get_card_with_external_data(self, card_code: str):
        """Get card with external data via service layer"""
        return await self.app_service.get_card_with_external_data(card_code)
    
    async def analyze_card_popularity(self, encounter: int):
        """Analyze card popularity via service layer"""
        return await self.app_service.analyze_card_popularity(encounter)