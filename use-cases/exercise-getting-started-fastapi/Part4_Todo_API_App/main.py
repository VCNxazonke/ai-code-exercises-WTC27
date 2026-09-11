"""
Exercise 4: Part 4 - Exercise Challenge
FastAPI To-Do List Application with CRUD, status filtering, completion, and deletion.
"""

from typing import List, Optional
from datetime import datetime, date
from enum import Enum
from fastapi import FastAPI, HTTPException, status, Query, Path
from pydantic import BaseModel, Field

class TodoStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Detailed task description")
    due_date: Optional[date] = Field(None, description="Optional target completion date")

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: TodoStatus
    created_at: datetime

app = FastAPI(
    title="FastAPI To-Do List Manager",
    description="Complete API for managing personal to-do tasks.",
    version="1.0.0"
)

# In-Memory Storage
todo_db = {}
todo_counter = 0


# 1. Create To-Do Item
@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    global todo_counter
    todo_counter += 1
    new_todo = {
        "id": todo_counter,
        "title": todo.title,
        "description": todo.description,
        "due_date": todo.due_date,
        "status": TodoStatus.PENDING,
        "created_at": datetime.utcnow()
    }
    todo_db[todo_counter] = new_todo
    return new_todo


# 2. List To-Do Items with Optional Status Filtering
@app.get("/todos/", response_model=List[TodoResponse])
async def list_todos(
    status_filter: Optional[TodoStatus] = Query(None, alias="status", description="Filter by status")
):
    todos = list(todo_db.values())
    if status_filter:
        todos = [t for t in todos if t["status"] == status_filter]
    return todos


# 3. Mark To-Do Item as Completed
@app.patch("/todos/{todo_id}/complete", response_model=TodoResponse)
async def complete_todo(todo_id: int = Path(..., gt=0)):
    if todo_id not in todo_db:
        raise HTTPException(status_code=404, detail=f"To-Do item {todo_id} not found.")
    todo_db[todo_id]["status"] = TodoStatus.COMPLETED
    return todo_db[todo_id]


# 4. Delete To-Do Item
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(..., gt=0)):
    if todo_id not in todo_db:
        raise HTTPException(status_code=404, detail=f"To-Do item {todo_id} not found.")
    del todo_db[todo_id]
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
