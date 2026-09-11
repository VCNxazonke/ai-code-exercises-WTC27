# Exercise 6: Part 3 - Simplified Concept Translation Guide

## 1. `asynccontextmanager` & Application Lifespan
- **Simplified Explanation:** The `@asynccontextmanager` decorator on `lifespan(app: FastAPI)` manages startup and shutdown tasks for the app.
- **Analogy:** It acts like turning the lights and equipment on when a restaurant opens (`print("Application startup")`), serving customers (`yield`), and turning off equipment and locking doors when closing (`print("Application shutdown")`).

## 2. `TimingMiddleware`
- **Simplified Explanation:** Middleware wraps around every HTTP request coming into the server.
- **Analogy:** It acts like a stopwatch at a drive-thru window. It presses "start" when a car arrives, lets the kitchen process the order (`call_next(request)`), presses "stop" when food is handed out, and writes the total processing time onto the receipt header (`X-Process-Time`).

## 3. JWT Authentication Flow
- **Simplified Explanation:** JSON Web Tokens act as digital concert wristbands.
- **Step 1 (Login):** User sends username/password to `/token`. Server verifies credentials and issues a signed JWT wristband containing user identity.
- **Step 2 (Request):** For subsequent requests (e.g., `/users/me`), client presents the JWT wristband.
- **Step 3 (Validation):** Server checks the signature on the wristband without querying the database password table again.
