# Exercise 2: Part 3 - Reflection Answers

## Question 1: How does FastAPI's approach to authentication compare to frameworks used before?
In traditional frameworks such as Django or Flask, authentication relies either on global session middleware or custom request decorators that manually extract HTTP headers, decode tokens, and attach user objects to global thread-local request contexts (`g.user` or `request.user`). FastAPI replaces manual header parsing with declarative dependency injection (`OAuth2PasswordBearer` and `Depends()`). The framework handles header extraction, scheme declaration for OpenAPI docs, and authentication error responses automatically before the request reaches the endpoint logic.

## Question 2: What advantages does FastAPI's dependency injection system provide for authentication?
FastAPI's dependency injection system (`Depends()`) enables clean composition and separation of security concerns. Authentication logic is broken down into modular, testable dependencies:
1. `OAuth2PasswordBearer`: Extracts the bearer token from incoming headers.
2. `get_current_user`: Decodes the JWT payload, validates credentials, and fetches the user object.
3. `get_current_active_user`: Depends on `get_current_user` and enforces active user status checks.

Route handlers declare `current_user: User = Depends(get_current_active_user)` as a parameter, making security dependencies explicit, reusable, and easy to mock during automated testing.

## Question 3: How does type hinting in FastAPI make security implementation clearer compared to other frameworks?
Type hints explicitly declare expected inputs and return types across security utilities and endpoints. For example, declaring `current_user: User` informs both the developer and static tools that `current_user` is a validated Pydantic `User` model with attributes like `.username` and `.email`. This eliminates guesswork regarding what data attributes exist on user objects, preventing runtime `AttributeError` crashes common in untyped framework request contexts.

## Question 4: What patterns from other frameworks can be identified in the JWT implementation?
Several standard web design patterns appear in FastAPI's JWT implementation:
- **Repository/Lookup Pattern:** `get_user()` encapsulates database query logic away from security handlers.
- **Middleware/Interceptor Pattern:** `OAuth2PasswordBearer` acts as an interceptor processing authorization headers before route execution.
- **Data Transfer Objects (DTO):** Pydantic `Token`, `TokenData`, and `User` schemas act as DTOs controlling serialization boundaries.
