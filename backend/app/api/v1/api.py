from fastapi import APIRouter
from app.api.v1.endpoints import cards, sync, analytics, scenarios, scoring, decks, context

api_router = APIRouter()

# Include all endpoint routers with proper prefixes and tags
api_router.include_router(
    cards.router,
    prefix="/cards",
    tags=["cards"],
)

api_router.include_router(
    decks.router,
    prefix="/decks",
    tags=["decks"],
)

api_router.include_router(
    sync.router,
    prefix="/sync",
    tags=["sync"],
)

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["analytics"],
)

api_router.include_router(
    scenarios.router,
    prefix="/scenarios",
    tags=["scenarios"],
)

api_router.include_router(
    scoring.router,
    prefix="/scoring",
    tags=["scoring"],
)

api_router.include_router(
    context.router,
    prefix="/context",
    tags=["context"],
)
