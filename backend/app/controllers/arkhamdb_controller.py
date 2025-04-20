import httpx

ARKHAMDB_CARDS_URL = "https://arkhamdb.com/api/public/cards/"

async def fetch_all_card_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ARKHAMDB_CARDS_URL}")
        response.raise_for_status()
        return response.json()
    
    
