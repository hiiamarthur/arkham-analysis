from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import get_async_db
from app.services.app_service import AppService
from app.services.arkhamdb_service import ArkhamDBService
from app.services.cache_service import cache_service
from app.services.deck_service import DeckService
from app.services.scenario_service import ScenarioService
from app.repositories.base_repositories import BaseRepository
from app.models.arkham_model import CardModel, TabooModel, TraitModel, EncounterSetModel

# Import scoring services
from app.services.card_service import CardService
from app.services.context_service import ContextService
from app.services.analysis_service import AnalysisService
from app.services.gpt_service import GPTService
from scoring_model.services import (
    BaseCardScoringService,
    ConservativeScoringService,
    AggressiveScoringService,
    ScenarioAwareScoringService,
    TempoScoringService,
    ControlScoringService,
    ComboScoringService,
)


# Database dependency (already exists)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency"""
    async for session in get_async_db():
        yield session


# Repository dependencies
async def get_card_repository(
    db: AsyncSession = Depends(get_db),
) -> BaseRepository[CardModel]:
    """Get shared card repository instance"""
    return BaseRepository(CardModel, db)


async def get_taboo_repository(
    db: AsyncSession = Depends(get_db),
) -> BaseRepository[TabooModel]:
    """Get shared taboo repository instance"""
    return BaseRepository(TabooModel, db)


async def get_trait_repository(
    db: AsyncSession = Depends(get_db),
) -> BaseRepository[TraitModel]:
    """Get shared trait repository instance"""
    return BaseRepository(TraitModel, db)


async def get_encounter_set_repository(
    db: AsyncSession = Depends(get_db),
) -> BaseRepository[EncounterSetModel]:
    """Get shared encounter set repository instance"""
    return BaseRepository(EncounterSetModel, db)


# Service dependencies - now with repository injection
async def get_app_service(
    db: AsyncSession = Depends(get_db),
    card_repo: BaseRepository[CardModel] = Depends(get_card_repository),
    taboo_repo: BaseRepository[TabooModel] = Depends(get_taboo_repository),
    trait_repo: BaseRepository[TraitModel] = Depends(get_trait_repository),
) -> AppService:
    """Get app service instance with injected repositories"""
    return AppService(db, card_repo, taboo_repo, trait_repo)


async def get_arkhamdb_service() -> ArkhamDBService:
    """Get ArkhamDB service instance"""
    return ArkhamDBService()


async def get_deck_service(
    arkhamdb_service: ArkhamDBService = Depends(get_arkhamdb_service)
) -> DeckService:
    """Get deck service instance with injected dependencies"""
    return DeckService(arkhamdb_service)


async def get_cache_service():
    """Get cache service instance"""
    return cache_service


async def get_card_service(
    db: AsyncSession = Depends(get_db),
    card_repo: BaseRepository[CardModel] = Depends(get_card_repository),
    deck_service: DeckService = Depends(get_deck_service),
) -> CardService:
    """Get card service instance with injected repositories and deck service"""
    return CardService(db, card_repo, deck_service)


async def get_scenario_service(
    db: AsyncSession = Depends(get_db),
    card_repo: BaseRepository[CardModel] = Depends(get_card_repository),
    encounter_set_repo: BaseRepository[EncounterSetModel] = Depends(
        get_encounter_set_repository
    ),
) -> ScenarioService:
    """Get scenario context service instance with shared card repository"""
    return ScenarioService(db, card_repo, encounter_set_repo)


# Scoring service dependencies
async def get_base_scoring_service() -> BaseCardScoringService:
    """Get base card scoring service"""
    return BaseCardScoringService()


async def get_conservative_scoring_service() -> ConservativeScoringService:
    """Get conservative scoring service"""
    return ConservativeScoringService()


async def get_aggressive_scoring_service() -> AggressiveScoringService:
    """Get aggressive scoring service"""
    return AggressiveScoringService()


async def get_scenario_aware_scoring_service(
    scenario_context: dict | None = None,
) -> ScenarioAwareScoringService:
    """Get scenario-aware scoring service"""
    return ScenarioAwareScoringService(scenario_context=scenario_context or {})


async def get_tempo_scoring_service() -> TempoScoringService:
    """Get tempo scoring service"""
    return TempoScoringService()


async def get_control_scoring_service() -> ControlScoringService:
    """Get control scoring service"""
    return ControlScoringService()


async def get_combo_scoring_service() -> ComboScoringService:
    """Get combo scoring service"""
    return ComboScoringService()


async def get_context_service() -> ContextService:
    """Get context service instance"""
    return ContextService()


async def get_gpt_service() -> GPTService:
    """Get GPT service instance"""
    return GPTService()


async def get_analysis_service(
    gpt_service: GPTService = Depends(get_gpt_service),
    context_service: ContextService = Depends(get_context_service),
    card_service: CardService = Depends(get_card_service),
    scenario_service: ScenarioService = Depends(get_scenario_service),
) -> AnalysisService:
    """Get analysis service instance with all dependencies"""
    return AnalysisService(gpt_service, context_service, card_service, scenario_service)


# Scoring service dependency (when you create it later)
# async def get_scoring_service(db: AsyncSession = Depends(get_db)) -> ScoringService:
#     """Get scoring service instance"""
#     return ScoringService(db)
