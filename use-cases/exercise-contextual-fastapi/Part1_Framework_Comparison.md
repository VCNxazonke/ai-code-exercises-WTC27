# Exercise 2: Part 1 - Framework Comparison Translation Table

This translation table maps core web framework concepts across Flask, Django, and FastAPI.

| Architectural Component | Flask Concept | Django Concept | FastAPI Equivalent | Key Architectural Differences |
| :--- | :--- | :--- | :--- | :--- |
| **Route Definition** | `@app.route('/path', methods=['GET'])` | `path('path/', view_func)` in `urls.py` | `@app.get('/path')` | FastAPI uses operation-specific decorators and automatic URL routing based on Python type hints. |
| **Request Data Validation** | Manual `request.args` / `request.json` parsing | Django Forms / Django REST Framework Serializers | Pydantic Models & Type Annotations | FastAPI automatically validates incoming JSON payloads against Pydantic models before entering the view handler. |
| **Dependency Injection & Middleware** | Custom `@app.before_request` hooks | Middleware classes in `MIDDLEWARE` setting | `Depends()` Dependency Injection System | FastAPI `Depends()` allows hierarchical, reusable dependency trees passed directly into route functions. |
| **Modular Organization** | `Blueprint` | `App` (`views.py`, `urls.py`) | `APIRouter` | `APIRouter` acts like Flask Blueprints, allowing modular prefixing, tagging, and middleware composition. |
| **Async Support** | Synchronous WSGI (Gunicorn / Flask default) | Synchronous WSGI / ASGI via channels | Native ASGI Async-First (Uvicorn / Starlette) | FastAPI natively executes non-blocking `async def` endpoints, dramatically scaling concurrent connections. |
