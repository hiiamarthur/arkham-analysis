# Repository Independence Patterns

## Your Question: "Repository Independence Across Services"

You asked whether repositories should be created independently across services or shared. Here are the patterns:

## ❌ Anti-Pattern: Service Creates Own Repositories

```python
# BAD: Each service creates its own repositories
class AppService:
    def __init__(self, db: AsyncSession):
        self.card_repo = BaseRepository(CardModel, db)  # ❌ New instance each time
        self.taboo_repo = BaseRepository(TabooModel, db)  # ❌ New instance each time

class ScenarioService:
    def __init__(self, db: AsyncSession):
        self.card_repo = BaseRepository(CardModel, db)  # ❌ Another new instance
```

**Problems:**
- Multiple instances of same repository type
- Harder to test (can't easily mock repositories)
- Tight coupling between services and repository implementation
- No repository lifecycle management

## ✅ Best Practice: Dependency Injection Pattern

```python
# GOOD: Repositories injected as dependencies
class AppService:
    def __init__(
        self, 
        db: AsyncSession,
        card_repo: BaseRepository[CardModel],
        taboo_repo: BaseRepository[TabooModel]
    ):
        self.db = db
        self.card_repo = card_repo  # ✅ Injected dependency
        self.taboo_repo = taboo_repo  # ✅ Injected dependency

class ScenarioService:
    def __init__(
        self, 
        db: AsyncSession,
        card_repo: BaseRepository[CardModel]  # ✅ Same repository instance
    ):
        self.db = db
        self.card_repo = card_repo  # ✅ Shared repository
```

**Benefits:**
- Single repository instance per request/scope
- Easy to mock for testing
- Loose coupling via dependency injection
- FastAPI manages lifecycle automatically

## 🏗️ FastAPI Dependency Injection Setup

```python
# app/api/deps.py
async def get_card_repository(db: AsyncSession = Depends(get_db)) -> BaseRepository[CardModel]:
    """Shared repository factory"""
    return BaseRepository(CardModel, db)

async def get_app_service(
    db: AsyncSession = Depends(get_db),
    card_repo: BaseRepository[CardModel] = Depends(get_card_repository)  # ✅ Shared
) -> AppService:
    return AppService(db, card_repo)

async def get_scenario_service(
    db: AsyncSession = Depends(get_db),
    card_repo: BaseRepository[CardModel] = Depends(get_card_repository)  # ✅ Same instance
) -> ScenarioService:
    return ScenarioService(db, card_repo)
```

## 🔄 Service-to-Service Communication Patterns

### Pattern 1: Service Calls Service (Current)
```python
# app/services/app_service.py
class AppService:
    async def sync_with_arkhamdb(self):
        # ✅ Service calls external service directly
        cards_data = await self.arkhamdb_service.fetch_all_card_data()
        return await self.process_cards(cards_data)

# Usage in endpoint:
async def sync_endpoint(app_service: AppService = Depends(get_app_service)):
    return await app_service.sync_with_arkhamdb()
```

### Pattern 2: Multiple Services in Endpoint
```python
# Alternative pattern for complex operations
async def complex_analysis_endpoint(
    app_service: AppService = Depends(get_app_service),
    scenario_service: ScenarioService = Depends(get_scenario_service),
    arkhamdb_service: ArkhamDBService = Depends(get_arkhamdb_service)
):
    """Endpoint orchestrates multiple services"""
    # ✅ Each service handles its domain
    cards = await app_service.get_cards_by_encounter(1)
    scenarios = await scenario_service.get_scenarios_for_cards([card.code for card in cards])
    external_data = await arkhamdb_service.fetch_taboo_data()
    
    # Business logic coordination happens in endpoint
    return {"cards": cards, "scenarios": scenarios, "external": external_data}
```

## 🧪 Testing Benefits

### Before (Hard to Test):
```python
# BAD: Hard to mock repositories
def test_app_service():
    service = AppService(mock_db)  # ❌ Creates real repositories internally
    # Can't easily mock repository behavior
```

### After (Easy to Test):
```python
# GOOD: Easy to mock dependencies
def test_app_service():
    mock_card_repo = Mock()
    mock_card_repo.get_first.return_value = mock_card_data
    
    service = AppService(mock_db, card_repo=mock_card_repo)  # ✅ Injected mock
    # Full control over repository behavior
```

## 📋 Repository Lifecycle

FastAPI's dependency system ensures:

1. **Request Scope**: Each HTTP request gets fresh repository instances
2. **Session Management**: Database sessions are properly closed
3. **Error Handling**: Automatic cleanup on exceptions
4. **Performance**: Connection pooling handled at DB layer

## 🎯 Key Takeaways

1. **Repositories should be shared dependencies**, not recreated in each service
2. **Use FastAPI's dependency injection** for repository management
3. **Services can share the same repository instance** within a request scope
4. **Repository independence** means each repository type has its own lifecycle, not that each service creates its own
5. **Testing becomes much easier** with dependency injection

Your updated code now follows the best practice pattern! 🚀