from fastapi import HTTPException
from app.schemas.card_schema import Card
from app.services.gpt_service import GPTService
from app.schemas.gpt_schema import OpenAIRequest, OpenAIResponse
import json


class GPTController:
    def __init__(self):
        self.gpt_service = GPTService()

    async def analyze_card(self, card: Card, db) -> dict:
        try:
            card_json = card.filter_card_for_prompt()
            request = OpenAIRequest(content=json.dumps(card_json))
            response: OpenAIResponse = await self.gpt_service.async_request(request, db)

            if not response.choices or not response.choices[0].message.content:
                raise HTTPException(status_code=400, detail="No response generated")

            # Parse the response content as JSON string
            content = json.loads(response.choices[0].message.content)
            return content

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
