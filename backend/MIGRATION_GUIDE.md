# API Restructure Migration Guide

## 🎯 What Changed

### Before (Controller Pattern):
```
routes/app_route.py → AppController → AppService
```

### After (FastAPI Native Pattern):
```  
api/v1/endpoints/cards.py → AppService (direct injection)
```

## 🔗 URL Changes

### NEW API Endpoints (Recommended):
| Old URL | New URL | Notes |
|---------|---------|-------|
| `/api/v1/app/card/{code}/` | `/api/v1/v1/cards/{code}` | Direct service injection |
| `/api/v1/app/cards/encounter/{encounter}` | `/api/v1/v1/cards/encounter/{encounter}/cards` | Better REST naming |
| `/api/v1/app/cards/search` | `/api/v1/v1/cards/search` | Same functionality |
| `/api/v1/app/fetch_cards/` | `/api/v1/v1/sync/cards` | Moved to sync domain |
| `/api/v1/app/get_taboos/` | `/api/v1/v1/sync/taboos` | Moved to sync domain |

### Legacy URLs (Still Work):
- `/api/v1/legacy/app/*` - All old endpoints with `/legacy` prefix

## 🏗️ Architecture Benefits

### ✅ NEW Structure Benefits:
1. **Direct Service Injection**: No controller layer overhead
2. **Domain Organization**: Cards, Sync, Analytics separated  
3. **Type Safety**: Better FastAPI integration
4. **Caching Headers**: Built into endpoints
5. **Error Handling**: Proper HTTP status codes

### 📝 Code Comparison:

#### OLD Pattern:
```python
# routes/app_route.py
@router.get("/card/{card_code}/")
async def get_card(card_code: str, db: AsyncSession = Depends(get_async_db)):
    controller = AppController(db=db)  # ❌ Extra instantiation
    return await controller.get_card(card_code)

# controllers/app_controller.py  
class AppController:
    def __init__(self, db: AsyncSession):
        self.app_service = AppService(db)
    
    async def get_card(self, card_id: str) -> Card:
        return await self.app_service.get_card(card_id)  # ❌ Just pass-through
```

#### NEW Pattern:
```python
# api/v1/endpoints/cards.py
@router.get("/{card_code}")
async def get_card(
    card_code: str,
    response: Response,
    app_service: AppService = Depends(get_app_service)  # ✅ Direct injection
):
    response.headers["Cache-Control"] = f"public, max-age={settings.CACHE_TTL_CARDS}"
    return await app_service.get_card(card_code)  # ✅ Direct call
```

## 🚀 Testing the New API

### Start the server:
```bash
cd backend
python app/main.py
```

### Test endpoints:
```bash
# NEW API (recommended)
curl http://localhost:8000/api/v1/v1/cards/01001
curl http://localhost:8000/api/v1/v1/cards/search?q=weapon
curl http://localhost:8000/api/v1/v1/sync/arkhamdb/health

# Legacy API (still works)
curl http://localhost:8000/api/v1/legacy/app/card/01001/
```

### Check API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 File Structure

### NEW:
```
app/
├── api/
│   ├── deps.py              # 🆕 Dependency injection
│   └── v1/
│       ├── api.py           # 🆕 Main API router  
│       └── endpoints/
│           ├── cards.py     # 🆕 Card operations
│           ├── sync.py      # 🆕 Sync operations
│           └── analytics.py # 🆕 Analytics operations
├── services/                # ✅ Same business logic
└── routes/                  # 🔄 Legacy (kept for backwards compatibility)
```

## 🎯 Next Steps

1. **Test new endpoints** with your frontend
2. **Update frontend** to use new URLs when ready
3. **Remove legacy routes** after migration complete
4. **Add scoring endpoints** using same pattern

## 🔧 Adding New Endpoints

Follow this pattern for new endpoints:

```python
# api/v1/endpoints/your_domain.py
from fastapi import APIRouter, Depends
from app.api.deps import get_app_service
from app.services.app_service import AppService

router = APIRouter()

@router.get("/your-endpoint")
async def your_function(
    param: str,
    service: AppService = Depends(get_app_service)  # ✅ Inject service directly
):
    return await service.your_method(param)
```

Then add to `api/v1/api.py`:
```python
from app.api.v1.endpoints import your_domain

api_router.include_router(
    your_domain.router,
    prefix="/your-domain", 
    tags=["your-domain"]
)
```

This gives you the FastAPI-native pattern while preserving your excellent service layer architecture!