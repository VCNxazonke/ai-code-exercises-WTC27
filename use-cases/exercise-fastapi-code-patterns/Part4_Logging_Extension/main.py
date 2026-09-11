"""
Exercise 6: Part 4 - Building Understanding Through Implementation
Extended FastAPI Code Patterns Application adding an Audit Log system.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Type, TypeVar, Generic, Callable
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from functools import wraps

# Database Models Base
class Base:
    pass

class User(Base):
    id: int
    username: str
    is_superuser: bool

    def __init__(self, id: int, username: str, is_superuser: bool = False):
        self.id = id
        self.username = username
        self.is_superuser = is_superuser

# NEW MODEL: Activity Audit Log
class AuditLog(Base):
    id: int
    user_id: str
    action: str
    timestamp: datetime

    def __init__(self, id: int, user_id: str, action: str, timestamp: Optional[datetime] = None):
        self.id = id
        self.user_id = user_id
        self.action = action
        self.timestamp = timestamp or datetime.utcnow()


# Generic Repository Pattern
T = TypeVar('T', bound=Base)

class Repository(Generic[T]):
    def __init__(self, storage_list: list):
        self.storage = storage_list

    def add(self, entity: T) -> T:
        self.storage.append(entity)
        return entity

    def list_all(self) -> List[T]:
        return self.storage

# In-Memory Storage Databases
db_users_list: List[User] = [
    User(id=1, username="admin_user", is_superuser=True),
    User(id=2, username="regular_user", is_superuser=False)
]
db_audit_logs_list: List[AuditLog] = []
audit_log_counter = 0

# Specialised Repositories
class UserRepository(Repository[User]):
    def get_by_username(self, username: str) -> Optional[User]:
        for u in self.storage:
            if u.username == username:
                return u
        return None

class AuditLogRepository(Repository[AuditLog]):
    def log_action(self, user_id: str, action: str) -> AuditLog:
        global audit_log_counter
        audit_log_counter += 1
        entry = AuditLog(id=audit_log_counter, user_id=user_id, action=action)
        return self.add(entry)


# Pydantic Schemas
class UserSchema(BaseModel):
    id: int
    username: str
    is_superuser: bool

class AuditLogSchema(BaseModel):
    id: int
    user_id: str
    action: str
    timestamp: datetime


# App Lifespan & Instance
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[SYSTEM] Starting server and initializing repositories...")
    yield
    print("[SYSTEM] Shutting down server...")

app = FastAPI(title="Advanced FastAPI Audit Pattern App", lifespan=lifespan)

# Dependencies & Auth
def get_user_repo() -> UserRepository:
    return UserRepository(db_users_list)

def get_audit_repo() -> AuditLogRepository:
    return AuditLogRepository(db_audit_logs_list)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repo)
) -> User:
    if token == "invalid":
        raise HTTPException(status_code=401, detail="Invalid token")
    user = user_repo.get_by_username(token)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def requires_role(role: str):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if role == "admin" and not current_user.is_superuser:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


# Routes
@app.post("/login")
async def login(
    username: str,
    user_repo: UserRepository = Depends(get_user_repo),
    audit_repo: AuditLogRepository = Depends(get_audit_repo)
):
    user = user_repo.get_by_username(username)
    if not user:
        audit_repo.log_action(user_id=username, action="FAILED_LOGIN")
        raise HTTPException(status_code=401, detail="Invalid username")
    
    audit_repo.log_action(user_id=username, action="SUCCESSFUL_LOGIN")
    return {"access_token": username, "token_type": "bearer"}


@app.get("/admin/audit-logs", response_model=List[AuditLogSchema])
@requires_role("admin")
async def get_audit_logs(
    current_user: User = Depends(get_current_user),
    audit_repo: AuditLogRepository = Depends(get_audit_repo)
):
    audit_repo.log_action(user_id=current_user.username, action="VIEWED_AUDIT_LOGS")
    return audit_repo.list_all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
