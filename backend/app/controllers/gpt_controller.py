from asyncio.log import logger
from fastapi import HTTPException
from app.schemas.card_schema import CardSchema
from app.services.gpt_service import GPTService
from app.schemas.gpt_schema import OpenAIRequest, OpenAIResponse
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.models.arkham_model import CardModel
from app.repositories.base_repositories import BaseRepository


class GPTController:
    def __init__(self, db: AsyncSession):
        self.gpt_service = GPTService()
        self.card_repo = BaseRepository(CardModel, db)

    async def analyze_card(self, cardCode: str) -> OpenAIResponse:
        try:
            cardData = await self.card_repo.get_first(
                filters={"filter_by[code][equals]": cardCode},
                include=["traits"],
                # filters={"code": cardCode}
            )
            if not cardData:
                raise HTTPException(status_code=404, detail="Card not found")

            card_json = CardSchema.from_model(cardData).filter_card_for_prompt()
            request = OpenAIRequest(content=json.dumps(card_json))
            response: OpenAIResponse = await self.gpt_service.async_request(request)

            # if not response.choices or not response.choices[0].message.content:
            #     raise HTTPException(status_code=400, detail="No response generated")

            # # Parse the response content as JSON string
            # content = json.loads(response.choices[0].message.content)
            # return cardData
            return response

        except Exception as e:
            logger.error(f"Error analyzing card: {e}")
            raise HTTPException(status_code=500, detail=str(e))
