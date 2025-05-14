from fastapi import APIRouter, Body, Depends
from app.controllers.app_controller import AppController
from app.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.gpt_controller import GPTController


router = APIRouter(prefix="/app", tags=["app"])


@router.get("/get_cards")
async def get_cards(db: AsyncSession = Depends(get_async_db)):
    controller = AppController(db=db)
    return await controller.get_cards()


@router.get("/get_taboos")
async def get_taboos(db: AsyncSession = Depends(get_async_db)):
    controller = AppController(db=db)
    return await controller.get_taboos()
