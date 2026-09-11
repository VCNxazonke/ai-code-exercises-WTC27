"""
Exercise 3: Part 4 - Comprehensive Documentation Challenge
RESTful Blog API with Auth, Blog Post CRUD, Comments, and Search.
"""

from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="FastAPI Comprehensive Blog API", version="1.0.0")

# In-Memory Database
db_users = {}
db_posts = {}
db_comments = {}
post_counter = 0
comment_counter = 0

# Schemas
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    username: str
    email: EmailStr

class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    tags: List[str] = Field(default=[])

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author: str
    tags: List[str]
    created_at: datetime

class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class CommentOut(BaseModel):
    id: int
    post_id: int
    author: str
    content: str
    created_at: datetime


# Dummy Authentication Dependency
def get_current_user_dummy(x_username: str = Query("demo_author")) -> str:
    """Simulates logged-in user identification via query param or header."""
    return x_username


# Routes: Auth
@app.post("/auth/register", response_model=UserOut, status_code=201)
async def register(user: UserRegister):
    if user.username in db_users:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_users[user.username] = user.dict()
    return user


# Routes: Blog Posts CRUD
@app.post("/posts/", response_model=PostOut, status_code=201)
async def create_post(
    post: PostCreate,
    current_user: str = Depends(get_current_user_dummy)
):
    global post_counter
    post_counter += 1
    new_post = {
        "id": post_counter,
        "title": post.title,
        "content": post.content,
        "author": current_user,
        "tags": post.tags,
        "created_at": datetime.utcnow()
    }
    db_posts[post_counter] = new_post
    return new_post


@app.get("/posts/", response_model=List[PostOut])
async def list_posts(
    search: Optional[str] = Query(None, description="Search in title or content"),
    tag: Optional[str] = Query(None, description="Filter by tag")
):
    results = list(db_posts.values())
    if search:
        s = search.lower()
        results = [p for p in results if s in p["title"].lower() or s in p["content"].lower()]
    if tag:
        results = [p for p in results if tag in p["tags"]]
    return results


@app.get("/posts/{post_id}", response_model=PostOut)
async def get_post(post_id: int = Path(..., gt=0)):
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_posts[post_id]


@app.delete("/posts/{post_id}", status_code=204)
async def delete_post(
    post_id: int = Path(..., gt=0),
    current_user: str = Depends(get_current_user_dummy)
):
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_posts[post_id]["author"] != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    del db_posts[post_id]
    return None


# Routes: Comments
@app.post("/posts/{post_id}/comments/", response_model=CommentOut, status_code=201)
async def create_comment(
    comment: CommentCreate,
    post_id: int = Path(..., gt=0),
    current_user: str = Depends(get_current_user_dummy)
):
    global comment_counter
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    comment_counter += 1
    new_comment = {
        "id": comment_counter,
        "post_id": post_id,
        "author": current_user,
        "content": comment.content,
        "created_at": datetime.utcnow()
    }
    db_comments[comment_counter] = new_comment
    return new_comment


@app.get("/posts/{post_id}/comments/", response_model=List[CommentOut])
async def list_comments(post_id: int = Path(..., gt=0)):
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return [c for c in db_comments.values() if c["post_id"] == post_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
