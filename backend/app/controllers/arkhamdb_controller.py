from typing import Any, Dict, List
import httpx
from app.core.config import settings

from app.models.arkham_model import CardModel
from app.schemas.card_schema import Card

ARKHAMDB_CARDS_URL = settings.ARKHAMDB_URL + "/public/cards/"
ARKHAMDB_TABOOS_URL = settings.ARKHAMDB_URL + "/public/taboos/"


class ArkhamDBController:
    async def fetch_all_card_data(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ARKHAMDB_CARDS_URL}")
            response.raise_for_status()
            return response.json()

    async def fetch_all_taboo_data(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ARKHAMDB_TABOOS_URL}")
            response.raise_for_status()
            return response.json()
