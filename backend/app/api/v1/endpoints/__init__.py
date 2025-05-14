from fastapi import APIRouter
from app.services.openai_service import OpenAIService

router = APIRouter()

@router.post("/generate")
async def generate_text(prompt: str):
    response = await OpenAIService.generate_response(prompt)
    return {"response": response} 