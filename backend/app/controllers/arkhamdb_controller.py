from typing import Any, Dict, List
import httpx
from app.core.config import settings

from app.models.arkham_model import CardModel
from app.schemas.card_schema import CardSchema
from app.services.arkhamdb_service import ArkhamDBService

ARKHAMDB_CARDS_URL = settings.ARKHAMDB_URL + "/public/cards/"
ARKHAMDB_TABOOS_URL = settings.ARKHAMDB_URL + "/public/taboos/"


class ArkhamDBController:

    def __init__(self):
        self.arkhamdb_service = ArkhamDBService()

    async def fetch_all_card_data(
        self, params: Dict[str, Any] = {}
    ) -> List[Dict[str, Any]]:
        return await self.arkhamdb_service.fetch_all_card_data(params)

    async def fetch_all_taboo_data(self) -> List[Dict[str, Any]]:
        return await self.arkhamdb_service.fetch_all_taboo_data()
