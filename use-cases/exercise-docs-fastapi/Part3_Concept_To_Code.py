"""
Exercise 3: Part 3 - Concept to Code Translation
Practical implementation of 5 core FastAPI documentation concepts:
1. Dependency Injection
2. Pydantic Models for Validation
3. Background Tasks
4. Path Operation Parameters
5. Exception Handling
"""

from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Path, Query, Header, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="Concept to Code Reference App")

# Concept 1: Dependency Injection
async def verify_token(x_token: str = Header(...)) -> str:
    if x_token != "secret-api-token":
        raise HTTPException(status_code=403, detail="Invalid API Token")
    return x_token


# Concept 2: Pydantic Validation Schemas
class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10)
    author_email: EmailStr
    tags: List[str] = Field(default=[])

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author_email: EmailStr
    tags: List[str]


# Concept 3: Background Tasks
def log_article_creation(article_id: int, title: str):
    print(f"[BACKGROUND TASK] Article {article_id} ('{title}') logged to audit service.")


@app.post("/articles/", response_model=ArticleResponse, status_code=201)
async def create_article(
    article: ArticleCreate,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token)
):
    created_id = 42
    background_tasks.add_task(log_article_creation, created_id, article.title)
    return {
        "id": created_id,
        "title": article.title,
        "content": article.content,
        "author_email": article.author_email,
        "tags": article.tags
    }


# Concept 4: Path Operation Parameters (Path, Query, Header)
@app.get("/articles/{article_id}")
async def read_article(
    article_id: int = Path(..., gt=0, description="Article ID must be positive"),
    include_comments: bool = Query(False, description="Whether to include comments"),
    user_agent: Optional[str] = Header(None)
):
    # Concept 5: Exception Handling
    if article_id == 999:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article {article_id} was not found."
        )
    
    return {
        "article_id": article_id,
        "title": f"Sample Article {article_id}",
        "include_comments": include_comments,
        "user_agent": user_agent
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
