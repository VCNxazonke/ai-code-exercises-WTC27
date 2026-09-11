# Exercise 2: Part 4 - Mental Model Translation Exercise

## Overview
This document maps traditional mental models from frameworks like Django and Flask to FastAPI architecture.

---

## Conceptual Architecture Mapping

```mermaid
flowchart LR
    subgraph Traditional Frameworks (Django / Flask)
        A[WSGI Gateway] --> B[Middleware Stack]
        B --> C[URL Router]
        C --> D[View Function / Controller]
        D --> E[Form / Serializer Validation]
        E --> F[ORM Database Query]
    end

    subgraph FastAPI Mental Model
        G[ASGI Uvicorn Engine] --> H[Starlette Middleware]
        H --> I[APIRouter + Type Hint Parser]
        I --> J[Pydantic Validation Boundary]
        J --> K[Depends Injection Hierarchy]
        K --> L[Async Operation Endpoint]
    end
```

---

## Component Translation Matrix

| Traditional Concept | FastAPI Counterpart | Architectural Adjustment |
| :--- | :--- | :--- |
| **Django `urls.py` / Flask `@app.route`** | `@app.get()`, `@app.post()`, `APIRouter` | Routes are declared alongside operation methods and type annotations directly in view files or router modules. |
| **Django Middleware / Flask `@app.before_request`** | `Depends()` / Starlette BaseHTTPMiddleware | Request filtering and dependency provision are declared per endpoint using `Depends()`, avoiding global overhead for endpoints that do not require specific middleware. |
| **Django Forms / DRF Serializers** | Pydantic `BaseModel` | Data schemas handle validation, parsing, serialization, and documentation generation seamlessly in one unified class definition. |
| **Global Request (`flask.request`)** | Injected parameters (`Request`, `Header`, `Query`, `Body`) | Instead of importing a thread-local request object, endpoints receive required headers, cookies, or body elements as explicit function arguments. |
| **Django Views / Flask Controllers** | Path operation functions (`async def endpoint(...)`) | View logic receives validated, typed parameters and dependency return values directly as function arguments. |
