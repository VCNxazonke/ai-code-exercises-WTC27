"""
Exercise 4: Part 2 - Creating Your First API
Basic FastAPI Application with Root, Path Parameters, and Query Parameters.
"""

from typing import Optional
from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(
    title="My First FastAPI App",
    description="A simple API demonstrating root, path, and query parameters.",
    version="0.1.0"
)

# 1. Root Endpoint
@app.get("/")
async def root():
    """Root endpoint returning a friendly JSON greeting."""
    return {"message": "Hello World from FastAPI!"}


# 2. Path Parameter Endpoint
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """Retrieves an item by its integer ID."""
    return {"item_id": item_id, "message": f"You requested item {item_id}"}


# 3. Query Parameter Endpoint
@app.get("/search/")
async def search_items(q: Optional[str] = None, skip: int = 0, limit: int = 10):
    """Searches for items using optional query parameters."""
    return {
        "query": q,
        "skip": skip,
        "limit": limit,
        "message": f"Searching for '{q}' (skipping {skip}, limit {limit})"
    }


if __name__ == "__main__":
    import uvicorn
    # Command to run manually: uvicorn main:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
