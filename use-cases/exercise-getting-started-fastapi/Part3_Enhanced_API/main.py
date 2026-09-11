"""
Exercise 4: Part 3 - Enhancing Your API
Structured FastAPI application with Pydantic models, custom exceptions, and modular routing.
"""

from typing import List, Optional
from fastapi import FastAPI, APIRouter, HTTPException, status, Path, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Models
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description")
    price: float = Field(..., gt=0, description="Price must be strictly positive")
    tags: List[str] = Field(default=[], description="Item search tags")

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

# Custom Exception Definition
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.message = f"Item with ID {item_id} was not found."
        super().__init__(self.message)

# Router Setup
router = APIRouter(prefix="/items", tags=["items"])
fake_items_db = {}
item_counter = 0


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    global item_counter
    item_counter += 1
    new_item = {**item.dict(), "id": item_counter}
    fake_items_db[item_counter] = new_item
    return new_item


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int = Path(..., gt=0)):
    if item_id not in fake_items_db:
        raise ItemNotFoundError(item_id)
    return fake_items_db[item_id]


@router.get("/", response_model=List[ItemResponse])
async def list_items(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    items = list(fake_items_db.values())
    return items[skip:skip + limit]


# Main App Initialization
app = FastAPI(
    title="Enhanced FastAPI Example",
    description="Modular API with custom exceptions and Pydantic validation",
    version="0.2.0"
)

# Exception Handlers
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message}
    )

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
