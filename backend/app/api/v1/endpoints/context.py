from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import Optional
from app.schemas.context_schema import (
    GameContextSchema,
    GameContextCreateRequest,
    GameContextResponse
)
from app.services.context_service import ContextService
from app.api.deps import get_context_service

# Import shared utilities
from . import (
    ARKHAM_HEADERS,
    CACHE_TTL_MEDIUM,
)

router = APIRouter()


@router.post("/game", response_model=GameContextResponse)
async def create_game_context(
    request: GameContextCreateRequest,
    response: Response,
    context_service: ContextService = Depends(get_context_service),
):
    """Create game context for GPT analysis"""
    try:
        stored_context = await context_service.store_game_context(request.game_context)
        
        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"private, max-age={CACHE_TTL_MEDIUM}"
        
        return GameContextResponse(
            success=True,
            message="Game context created successfully",
            game_context=stored_context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create game context: {str(e)}"
        )


@router.get("/game", response_model=GameContextResponse)
async def get_game_context(
    response: Response,
    session_id: Optional[str] = None,
    context_service: ContextService = Depends(get_context_service),
):
    """Get game context for analysis"""
    try:
        game_context = await context_service.get_game_context(session_id)
        
        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"private, max-age={CACHE_TTL_MEDIUM}"
        
        return GameContextResponse(
            success=True,
            message="Game context retrieved successfully",
            game_context=game_context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game context not found: {str(e)}"
        )


@router.put("/game", response_model=GameContextResponse)
async def update_game_context(
    request: GameContextCreateRequest,
    response: Response,
    session_id: Optional[str] = None,
    context_service: ContextService = Depends(get_context_service),
):
    """Update existing game context"""
    try:
        updated_context = await context_service.update_game_context(
            session_id, request.game_context
        )
        
        response.headers.update(ARKHAM_HEADERS)
        
        return GameContextResponse(
            success=True,
            message="Game context updated successfully",
            game_context=updated_context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update game context: {str(e)}"
        )


@router.delete("/game")
async def delete_game_context(
    response: Response,
    session_id: Optional[str] = None,
    context_service: ContextService = Depends(get_context_service),
):
    """Delete game context"""
    try:
        await context_service.delete_game_context(session_id)
        
        response.headers.update(ARKHAM_HEADERS)
        
        return {"success": True, "message": "Game context deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete game context: {str(e)}"
        )