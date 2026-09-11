# Exercise 3: Part 2 - Documentation Deep Dive: `Depends` & Security

## Deep Dive Notes: The `Depends()` System

### Core Purpose
`Depends()` is FastAPI's mechanism for **Dependency Injection**. It allows functions (dependencies) to be declared as prerequisites for route handlers. When a request arrives, FastAPI automatically executes the dependency function, resolves any sub-dependencies, and passes the return value to the endpoint parameter.

### Key Capabilities & Patterns
- **Code Reuse:** Shared logic (such as parameter parsing or database session management) is written once and reused across multiple routes.
- **Hierarchical Trees:** Dependencies can depend on other dependencies, building a clean execution chain.
- **Context Managers / Yield Dependencies:** Dependencies using `yield` perform setup before returning a resource (e.g., opening a database session) and cleanup afterward (e.g., closing the session), even if exceptions occur during request handling.

---

## Security Documentation Summary

FastAPI's security utilities (`fastapi.security`) build upon the dependency injection system:
- **`OAuth2PasswordBearer`:** Declares an OAuth2 password flow with a bearer token URL, enabling Swagger UI interactive authorization buttons.
- **HTTP Bearer / HTTP Basic:** Built-in schemes for standard authorization headers.
- **Security Scopes:** Allows fine-grained permission enforcement (e.g., `me`, `items:read`, `items:write`) directly within route parameter declarations.
