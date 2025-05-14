from fastapi import APIRouter
from app.controllers.arkhamdb_controller import ArkhamDBController
from pydantic import BaseModel

router = APIRouter(prefix="/arkhamdb", tags=["arkhamdb"])
controller = ArkhamDBController()


class CardResponse(BaseModel):
    id: str
    name: str
    type: str
    data: dict


@router.get("/get_cards")
async def get_cards():
    """
    Get all Arkham Horror cards.
    """
    return await controller.fetch_all_card_data()


# @router.get("/card/{card_id}", response_model=CardResponse)
# async def get_card(card_id: str):
#     """
#     Get a specific card by ID.
#     Returns a validated CardResponse object.
#     """
#     return controller.get_card(card_id)
