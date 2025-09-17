from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import Optional
from app.schemas.context_schema import (
    UserContextSchema,
    UserContextCreateRequest,
    UserContextResponse
)
from app.services.context_service import ContextService
from app.api.deps import get_context_service

# Import shared utilities
from . import (
    ARKHAM_HEADERS,
    CACHE_TTL_MEDIUM,
)

router = APIRouter()


@router.post("/user", response_model=UserContextResponse)
async def create_user_context(
    request: UserContextCreateRequest,
    response: Response,
    context_service: ContextService = Depends(get_context_service),
):
    """Create or update user context for personalized analysis"""
    try:
        # Store user context (you might want to add user authentication here)
        stored_context = await context_service.store_user_context(request.user_context)
        
        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"private, max-age={CACHE_TTL_MEDIUM}"
        
        return UserContextResponse(
            success=True,
            message="User context created successfully",
            user_context=stored_context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user context: {str(e)}"
        )


@router.get("/user", response_model=UserContextResponse)
async def get_user_context(
    response: Response,
    user_id: Optional[str] = None,  # In a real app, get from auth
    context_service: ContextService = Depends(get_context_service),
):
    """Get user context for personalized analysis"""
    try:
        user_context = await context_service.get_user_context(user_id)
        
        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"private, max-age={CACHE_TTL_MEDIUM}"
        
        return UserContextResponse(
            success=True,
            message="User context retrieved successfully",
            user_context=user_context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User context not found: {str(e)}"
        )


@router.put("/user", response_model=UserContextResponse)
async def update_user_context(
    request: UserContextCreateRequest,
    response: Response,
    user_id: Optional[str] = None,  # In a real app, get from auth
    context_service: ContextService = Depends(get_context_service),
):
    """Update existing user context"""
    try:
        updated_context = await context_service.update_user_context(
            user_id, request.user_context
        )
        
        response.headers.update(ARKHAM_HEADERS)
        
        return UserContextResponse(
            success=True,
            message="User context updated successfully",
            user_context=updated_context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update user context: {str(e)}"
        )


@router.delete("/user")
async def delete_user_context(
    response: Response,
    user_id: Optional[str] = None,  # In a real app, get from auth
    context_service: ContextService = Depends(get_context_service),
):
    """Delete user context"""
    try:
        await context_service.delete_user_context(user_id)
        
        response.headers.update(ARKHAM_HEADERS)
        
        return {"success": True, "message": "User context deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete user context: {str(e)}"
        )