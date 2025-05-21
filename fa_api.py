from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
import json

app = FastAPI(
    title="Financial Advisor API",
    description="API for retrieving financial advisor and client information",
    version="1.0.0"
)

def load_data() -> List[Dict[str, Any]]:
    """Load the client data from JSON file."""
    with open('data.json', 'r') as f:
        return json.load(f)

@app.get("/api/fa/{fa_name}/clients")
async def get_client_details_by_fa_name(fa_name: str) -> List[Dict[str, Any]]:
    """Retrieve all client details associated with the given FA_NAME."""
    data = load_data()
    clients = [client for client in data if client['FA_NAME'] == fa_name]
    if not clients:
        raise HTTPException(status_code=404, detail=f"No clients found for FA: {fa_name}")
    return clients

@app.get("/api/fa")
async def get_all_fa_names() -> List[str]:
    """Return the list of all unique Financial Advisor names."""
    data = load_data()
    return list(set(client['FA_NAME'] for client in data))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 