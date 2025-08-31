from fastapi import APIRouter, Body, Depends
from app.controllers.app_controller import AppController
from app.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.gpt_controller import GPTController


router = APIRouter(prefix="/app", tags=["app"])


@router.post("/fetch_cards/")
async def fetch_cards(encounter: int = 1, db: AsyncSession = Depends(get_async_db)):
    controller = AppController(db=db)
    return await controller.fetch_cards(encounter=encounter)


@router.get("/card/{card_code}/")
async def get_card(card_code: str, db: AsyncSession = Depends(get_async_db)):
    controller = AppController(db=db)
    return await controller.get_card(card_code)


@router.get("/get_taboos/")
async def get_taboos(db: AsyncSession = Depends(get_async_db)):
    controller = AppController(db=db)
    return await controller.get_taboos()
