# Exercise 6: Part 2 - Request Execution Flow Trace (`/admin/users/`)

## Request Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Middleware as TimingMiddleware
    participant Router as APIRouter
    participant RBAC as @requires_role("admin")
    participant AuthDep as get_current_user
    participant DBDep as get_db
    participant Repo as UserRepository
    participant Endpoint as list_users Endpoint

    Client->>Middleware: GET /admin/users/ (Bearer Header)
    Middleware->>Middleware: Record start_time
    Middleware->>Router: Dispatch Request
    Router->>RBAC: Intercept Execution
    RBAC->>AuthDep: Resolve dependency (token)
    AuthDep->>DBDep: Acquire AsyncSession
    DBDep-->>AuthDep: Yield active db session
    AuthDep->>AuthDep: Decode & validate JWT payload
    AuthDep->>Repo: get_by_username(db, username)
    Repo-->>AuthDep: Return User entity
    AuthDep-->>RBAC: Return authenticated User
    RBAC->>RBAC: Check if current_user.is_superuser == True
    alt User is Not Superuser
        RBAC-->>Client: HTTP 403 Forbidden Exception
    else User is Admin Superuser
        RBAC->>Endpoint: Execute list_users(skip, limit, db)
        Endpoint->>Repo: list(db, skip, limit)
        Repo-->>Endpoint: Return List[User]
        Endpoint-->>Middleware: Return User list response
        Middleware->>Middleware: Calculate elapsed ms & set X-Process-Time header
        Middleware-->>Client: Return HTTP 200 OK + JSON Users List
    end
    DBDep->>DBDep: Close AsyncSession (finally block)
```

---

## Step-by-Step Execution Narrative

1. **HTTP Request Entry:** Client issues `GET /admin/users/` with Authorization Header (`Bearer <token>`).
2. **Middleware Interception:** `TimingMiddleware` intercepts the request and records `start_time = datetime.utcnow()`.
3. **Route & Decorator Matching:** Router selects `list_users` and encounters `@requires_role("admin")`.
4. **Dependency Resolution (`get_db`):** Opens an async database session via `get_db()` context manager.
5. **Authentication Resolution (`get_current_user`):** Decodes JWT token, extracts `sub` username, queries `UserRepository`, and retrieves the user object.
6. **Authorization Check:** `@requires_role` verifies `current_user.is_superuser`. If false, raises HTTP 403.
7. **Endpoint Logic Execution:** `list_users` queries `UserRepository.list()` to fetch user records.
8. **Response Processing & Header Enrichment:** `TimingMiddleware` calculates total elapsed execution time in milliseconds and attaches header `X-Process-Time`.
9. **Session Cleanup:** `get_db` closes the database session in its `finally` block.
