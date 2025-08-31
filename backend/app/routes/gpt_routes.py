from fastapi import APIRouter, Depends
from app.controllers.gpt_controller import GPTController
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.schemas.card_schema import Card

router = APIRouter(prefix="/gpt", tags=["gpt"])


class AnalyzeCardRequest(BaseModel):
    cardCode: str


@router.post("/analyze_card/")
async def analyze_card(
    request: AnalyzeCardRequest, db: AsyncSession = Depends(get_async_db)
):
    controller = GPTController(db)
    return await controller.analyze_card(request.cardCode)
