# FastAPI Request Patterns Guide

## ❓ Your Question: GET Request with Request Body vs Query Parameters

You correctly identified that **GET requests should use query/path parameters**, not request body models.

## 🔄 Fixed Pattern

### ❌ Before: GET with Request Body (Wrong)
```python
class ScenarioContextRequest(BaseModel):  # ❌ Request body for GET
    scenario_code: str
    difficulty: Difficulty
    no_of_investigators: int

@router.get("/{scenario_code}/context")
async def get_scenario_context(
    scenario_context_request: ScenarioContextRequest  # ❌ Body in GET
):
    pass
```

### ✅ After: GET with Query Parameters (Correct)
```python
# ✅ No request body model needed for GET

@router.get("/{scenario_code}/context")
async def get_scenario_context(
    scenario_code: str,  # ✅ Path parameter
    difficulty: Difficulty = Query(Difficulty.STANDARD),  # ✅ Query parameter
    no_of_investigators: int = Query(4, ge=1, le=4),     # ✅ Query parameter
):
    pass
```

## 📋 FastAPI Request Parameter Types

### 🛣️ Path Parameters
```python
@router.get("/scenarios/{scenario_code}/chaos-tokens")
async def get_chaos_tokens(
    scenario_code: str,  # ✅ From URL path
):
    pass

# Example URL: /scenarios/the_gathering/chaos-tokens
```

### 🔍 Query Parameters  
```python
@router.get("/scenarios/")
async def get_scenarios(
    campaign: Optional[CampaignType] = Query(None),    # ✅ ?campaign=dunwich
    difficulty: Difficulty = Query(Difficulty.STANDARD) # ✅ &difficulty=expert
):
    pass

# Example URL: /scenarios/?campaign=dunwich&difficulty=expert
```

### 📝 Request Body (POST/PUT/PATCH only)
```python
class ScenarioAnalysisRequest(BaseModel):  # ✅ For POST requests
    scenario_code: str
    difficulty: Difficulty
    include_probabilities: bool

@router.post("/scenarios/{scenario_code}/analyze")  # ✅ POST uses body
async def analyze_scenario(
    scenario_code: str,                              # ✅ Path parameter
    analysis_request: ScenarioAnalysisRequest       # ✅ Request body
):
    pass
```

## 🎯 When to Use Each Pattern

### GET Requests - Retrieve Data
```python
# ✅ Use Query + Path parameters
@router.get("/scenarios/{scenario_code}")
async def get_scenario(
    scenario_code: str,                    # Path: identifies resource
    difficulty: Difficulty = Query(...)   # Query: filters/options
):
    pass

# Call: GET /scenarios/the_gathering?difficulty=expert
```

### POST Requests - Create or Complex Operations
```python
# ✅ Use Request Body for complex data
@router.post("/scenarios/compare")
async def compare_scenarios(
    comparison_request: ScenarioComparisonRequest  # Body: complex data
):
    pass

# Call: POST /scenarios/compare
# Body: {"scenario_codes": ["the_gathering", "midnight_masks"], "difficulty": "expert"}
```

## 🛠️ Your Fixed Scenario Endpoints

### GET - Query Parameters
```python
# ✅ Fixed: Using query parameters
@router.get("/{scenario_code}/context")
async def get_scenario_context(
    scenario_code: str,                                    # Path
    difficulty: Difficulty = Query(Difficulty.STANDARD),  # Query  
    no_of_investigators: int = Query(4, ge=1, le=4)       # Query
):
    # URL: /the_gathering/context?difficulty=expert&no_of_investigators=2
    pass
```

### POST - Request Body
```python
# ✅ Correct: Complex analysis with request body
@router.post("/{scenario_code}/analyze")
async def analyze_scenario(
    scenario_code: str,                        # Path
    analysis_request: ScenarioAnalysisRequest # Body (complex data)
):
    pass
```

## 📊 Request Body vs Query Parameters

| **Aspect** | **Query Parameters** | **Request Body** |
|------------|---------------------|------------------|
| **HTTP Methods** | GET, DELETE | POST, PUT, PATCH |
| **Data Complexity** | Simple values | Complex objects |
| **URL Length** | Limited by URL length | No limit |
| **Caching** | Cacheable | Not cacheable |
| **Visibility** | Visible in URL/logs | Hidden in body |

## 🧪 Testing Examples

### GET with Query Parameters
```bash
# ✅ Simple and clear
curl "http://localhost:8000/api/v1/scenarios/the_gathering/context?difficulty=expert&no_of_investigators=2"
```

### POST with Request Body
```bash
# ✅ Complex data structure
curl -X POST "http://localhost:8000/api/v1/scenarios/the_gathering/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_code": "the_gathering",
    "difficulty": "expert", 
    "include_probabilities": true,
    "investigator_count": 2
  }'
```

## 🎯 Key Takeaways

1. **GET requests** → Use `Query()` and path parameters
2. **POST requests** → Use request body models (`BaseModel`)  
3. **Simple data** → Query parameters
4. **Complex data** → Request body
5. **Resource identification** → Path parameters
6. **Filtering/options** → Query parameters

Your instinct was 100% correct - GET requests should use query parameters, not request bodies! 🎉