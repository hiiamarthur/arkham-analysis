# Encounter Set Architecture Decision

## 🎯 Your Question: Database vs Enum for Encounter Types?

**Answer:** **Database approach** (like traits) is recommended over hardcoded enums for encounter sets.

## 🏗️ Implementation Comparison

### ❌ Enum Approach (Too Rigid):
```python
# app/domain/game_types.py
class EncounterSet(Enum):
    CORE = "core"
    STRIKING_FEAR = "striking_fear"
    ANCIENT_EVILS = "ancient_evils"
    # ❌ Hard to maintain
    # ❌ No metadata (pack info, size, etc.)
    # ❌ Can't sync from ArkhamDB
```

### ✅ Database Approach (Recommended):
```python
# app/models/arkham_model.py
class EncounterSetModel(BaseModel):
    id: int
    code: str                    # ✅ "striking_fear"
    name: str                    # ✅ "Striking Fear"
    pack_code: str               # ✅ "core"
    pack_name: str               # ✅ "Core Set"
    cycle_name: str              # ✅ "Core"
    size: int                    # ✅ 7 cards
    is_unique: bool              # ✅ False (reusable set)
    
    # ✅ Rich relationships
    cards: List[CardModel]       # ✅ Actual cards in this set
```

## 🎯 Why Database Wins

### 1. **Dynamic Content**
```python
# ✅ New encounter sets automatically available
encounter_sets = await encounter_repo.get_all()  # Gets latest from ArkhamDB

# ❌ Enum requires code changes
class EncounterSet(Enum):
    NEW_SET = "new_set"  # Must add manually for each release
```

### 2. **Rich Metadata**
```python
# ✅ Database stores complete information
{
    "code": "striking_fear",
    "name": "Striking Fear", 
    "pack_name": "Core Set",
    "cycle_name": "Core",
    "size": 7,
    "card_count": 7,
    "is_unique": False
}

# ❌ Enum only has basic info
EncounterSet.STRIKING_FEAR.value  # Just "striking_fear"
```

### 3. **Flexible Relationships**
```python
# ✅ Database: Cards can belong to multiple encounter sets
card = await card_repo.get_with_encounter_sets("01001")
print(f"Card belongs to: {[es.name for es in card.encounter_sets]}")

# ❌ Enum: No relationship support
```

### 4. **ArkhamDB Synchronization**
```python
# ✅ Database: Sync from external API
async def sync_encounter_sets():
    arkham_data = await arkhamdb_service.fetch_encounter_sets()
    for set_data in arkham_data:
        encounter_set = EncounterSetModel(**set_data)
        db.add(encounter_set)

# ❌ Enum: Manual code updates required
```

## 🚀 API Benefits

### Encounter Set Endpoints
```python
# app/api/v1/endpoints/encounter_sets.py

@router.get("/encounter-sets/", response_model=List[EncounterSetSummary])
async def get_encounter_sets(
    cycle: Optional[str] = Query(None),  # Filter by cycle
    pack: Optional[str] = Query(None),   # Filter by pack
):
    """Get all encounter sets with filtering"""
    # ✅ Dynamic filtering from database
    return await encounter_repo.get_all(cycle=cycle, pack=pack)

@router.get("/encounter-sets/{code}/cards")
async def get_encounter_set_cards(code: str):
    """Get all cards in an encounter set"""  
    # ✅ Rich card relationships
    encounter_set = await encounter_repo.get_with_cards(code)
    return encounter_set.cards
```

### Example API Responses
```json
GET /api/v1/encounter-sets/?cycle=core

[
    {
        "code": "striking_fear",
        "name": "Striking Fear",
        "cycle_name": "Core",
        "card_count": 7
    },
    {
        "code": "ancient_evils", 
        "name": "Ancient Evils",
        "cycle_name": "Core",
        "card_count": 3
    }
]
```

## 🔧 Service Integration

```python
# app/services/app_service.py
class AppService:
    
    async def get_scenario_encounter_sets(self, scenario_code: str) -> List[EncounterSet]:
        """Get encounter sets for a scenario"""
        # ✅ Database lookup with rich data
        scenario = await self.get_scenario_by_code(scenario_code)
        encounter_sets = await self.encounter_repo.get_by_scenario(scenario.id)
        return [EncounterSet.from_model(es) for es in encounter_sets]
    
    async def sync_encounter_sets_from_arkhamdb(self):
        """Sync encounter sets from ArkhamDB"""
        # ✅ Dynamic content updates
        arkham_data = await self.arkhamdb_service.fetch_encounter_sets()
        
        for set_data in arkham_data:
            existing = await self.encounter_repo.get_by_code(set_data["code"])
            if existing:
                await self.encounter_repo.update(existing.id, set_data)
            else:
                await self.encounter_repo.create(set_data)
```

## 📊 Database vs Enum Summary

| **Aspect** | **Database** | **Enum** |
|------------|--------------|----------|
| **Dynamic Content** | ✅ Auto-sync from ArkhamDB | ❌ Manual code changes |
| **Metadata** | ✅ Pack, cycle, size, etc. | ❌ Just name/code |
| **Relationships** | ✅ Cards, scenarios | ❌ No relationships |
| **Filtering** | ✅ Complex queries | ❌ Limited filtering |
| **Maintenance** | ✅ Data-driven updates | ❌ Code releases required |
| **Performance** | ✅ Indexed queries | ✅ In-memory (faster) |

## 🎯 Implementation Status

### ✅ What's Done:
1. **EncounterSetModel** - Database model with relationships
2. **Association Table** - `card_encounter_sets` for many-to-many
3. **Schema Classes** - Pydantic models for API
4. **Card Relationship** - Cards can have multiple encounter sets

### 🔄 Next Steps:
1. **Migration** - Create database tables
2. **Repository** - CRUD operations for encounter sets  
3. **Service Integration** - Add to app service
4. **API Endpoints** - Encounter set endpoints
5. **ArkhamDB Sync** - Fetch encounter set data

## 🏆 Recommendation

Use the **database approach** for encounter sets because:
- **Future-proof** - New sets automatically supported
- **Rich data** - Complete metadata from ArkhamDB  
- **Flexible** - Complex queries and relationships
- **Maintainable** - No code changes for content updates

This follows the same successful pattern you used for traits! 🎯