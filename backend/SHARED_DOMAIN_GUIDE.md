# Shared Domain Architecture Guide

## ✅ Solution: Shared Domain Folder

Your question about sharing enums and static classes between the scoring model and FastAPI has been solved by creating a **shared domain layer**.

## 🏗️ Architecture Overview

```
backend/
├── app/
│   ├── domain/                    # 🆕 Shared domain types
│   │   ├── __init__.py           # Exports all domain types
│   │   ├── difficulty.py         # Game difficulty levels
│   │   ├── campaigns.py          # Campaign definitions  
│   │   ├── scenarios.py          # Scenario types & modifications
│   │   └── game_types.py         # Card types, factions, etc.
│   └── api/v1/endpoints/         # FastAPI endpoints use domain types
├── scoring_model/
│   └── Scenario/
│       └── __init__.py           # 🔄 Now imports from shared domain
```

## 🎯 What Was Moved

### From `scoring_model/Scenario/__init__.py`:
- ✅ `Difficulty` enum → `app/domain/difficulty.py`
- ✅ `CAMPAIGNTYPE` enum → `app/domain/campaigns.py` 
- ✅ `ScenarioType` enum → `app/domain/scenarios.py`
- ✅ `SCENARIO_MODIFICATIONS` → `app/domain/scenarios.py`

### Added to FastAPI:
- ✅ `CardType`, `Faction` enums → `app/domain/game_types.py`
- ✅ Shared validation, response models → `app/api/v1/endpoints/__init__.py`

## 🔗 How They Connect

### 1. FastAPI Uses Shared Domain Types
```python
# app/api/v1/endpoints/scenarios.py
from domain import Difficulty, CampaignType, ScenarioType, get_scenario_modifications

@router.get("/{scenario_code}/chaos-tokens")
async def get_scenario_chaos_tokens(
    scenario_code: str,
    difficulty: Difficulty = Query(Difficulty.STANDARD)  # ✅ Shared enum
):
    # ✅ Uses shared domain logic
    modifications = get_scenario_modifications(scenario, difficulty)
```

### 2. Scoring Model Uses Shared Domain Types
```python
# scoring_model/Scenario/__init__.py
from domain import Difficulty, CampaignType as CAMPAIGNTYPE, ScenarioType

class Scenario(ABC):
    def __init__(self, campaign: Campaign, scenario: ScenarioType, difficulty: Difficulty):
        # ✅ Same enums as FastAPI uses
        self.scenario_modifications = get_scenario_modifications(scenario, difficulty)
```

### 3. Backwards Compatibility Maintained
```python
# scoring_model/Scenario/__init__.py  
def get_scenario_modifications_compat(scenario: ScenarioType, difficulty: Difficulty):
    """Backwards compatibility wrapper"""
    return get_scenario_modifications(scenario, difficulty)
```

## 🚀 New API Endpoints

Your shared domain types enable new API functionality:

### Scenarios API
```bash
# Get all scenarios
GET /api/v1/scenarios/

# Get chaos token modifications 
GET /api/v1/scenarios/the_gathering/chaos-tokens?difficulty=expert

# Compare difficulties
GET /api/v1/scenarios/the_gathering/difficulty-comparison
```

### Example Response:
```json
{
  "scenario": {
    "code": "the_gathering",
    "name": "The Gathering", 
    "campaign": "night_of_the_zealot"
  },
  "difficulty": "expert",
  "token_modifications": {
    "skull": {
      "effect": "-2. If you fail, after this skill test, search the encounter deck...",
      "value": "2"
    }
  }
}
```

## 🎯 Benefits of This Approach

### ✅ Single Source of Truth
- Enums defined once in `app/domain/`
- Both FastAPI and scoring model import from same source
- No duplication or inconsistencies

### ✅ Type Safety
```python
# Both systems use the same types
difficulty: Difficulty = Difficulty.EXPERT         # ✅ Same enum
scenario: ScenarioType = ScenarioType.THE_GATHERING # ✅ Same enum
```

### ✅ Easy Maintenance
- Add new campaign: Update `app/domain/campaigns.py` → Available everywhere
- Add new scenario: Update `app/domain/scenarios.py` → API and scoring model both get it

### ✅ Clear Separation
```
🏗️ Domain Layer:    Pure business logic, no dependencies
📡 API Layer:       Uses domain types for validation/responses  
🧠 Scoring Layer:   Uses domain types for game calculations
```

## 🔧 Adding New Content

### New Campaign:
```python
# app/domain/campaigns.py
class CampaignType(Enum):
    # existing campaigns...
    THE_NEW_CAMPAIGN = "the_new_campaign"  # ✅ Add here
```

### New Scenario:
```python  
# app/domain/scenarios.py
class ScenarioType(Enum):
    # existing scenarios...
    NEW_SCENARIO = (CampaignType.THE_NEW_CAMPAIGN, "new_scenario")  # ✅ Add here
```

### Automatically Available In:
- ✅ FastAPI validation (`/scenarios/` endpoint)
- ✅ Scoring model chaos bag setup
- ✅ API documentation (Swagger/OpenAPI)
- ✅ Type checking and IDE autocomplete

## 🧪 Testing Integration

```python
# Test both systems use same types
from domain import ScenarioType, Difficulty
from scoring_model.Scenario import create_night_of_zealot_scenario

def test_shared_types():
    # ✅ Same enum works in both systems
    scenario = create_night_of_zealot_scenario(
        Difficulty.EXPERT, 
        ScenarioType.THE_GATHERING
    )
    assert scenario.difficulty == Difficulty.EXPERT
```

## 📋 Next Steps

1. **Add More Scenarios**: Extend `app/domain/scenarios.py` with remaining scenarios
2. **Enhance API**: Use shared types for deck building, card filtering
3. **Scoring Integration**: Connect scoring model calculations to FastAPI endpoints
4. **Frontend Types**: Generate TypeScript definitions from shared domain types

The shared domain approach gives you the best of both worlds: **separation of concerns** while **sharing domain knowledge**! 🎉