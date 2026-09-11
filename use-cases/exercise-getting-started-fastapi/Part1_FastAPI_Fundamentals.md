# Exercise 4: Part 1 - FastAPI Fundamentals & Glossary

## Overview of FastAPI
FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints.

### Key Advantages
- **Fast:** Very high performance, on par with Node.js and Go (thanks to Starlette and Pydantic).
- **Fast to Code:** Increases feature development speed by 200% to 300%.
- **Fewer Bugs:** Reduces human-induced developer errors by approximately 40%.
- **Intuitive:** Great editor support with complete autocompletion everywhere.
- **Standards-based:** Fully compliant with OpenAPI and JSON Schema specifications.

---

## Essential FastAPI Glossary

- **ASGI (Asynchronous Server Gateway Interface):** The modern standard interface between async Python web servers (like Uvicorn) and web applications.
- **Uvicorn:** A lightning-fast ASGI server implementation used to run FastAPI applications.
- **Path Operation Decorator:** Decorator functions like `@app.get("/")` or `@app.post("/items/")` that associate HTTP verbs and paths with Python handler functions.
- **Path Parameter:** Variable parts of a URL path (e.g., `/items/{item_id}`) captured and passed as typed arguments to endpoint functions.
- **Query Parameter:** Key-value pairs appended to URLs after `?` (e.g., `/items?skip=0&limit=10`) used for filtering and pagination.
- **Pydantic Model:** Data validation and serialization class defined using standard Python type annotations.
