# Activity 2: Code Quality Detective Review

## Legacy Code Evaluation
The code review inspected an old Python data processing module containing monolithic control structures, broad exception handling (`except Exception:`), string concatenation for database queries, and inconsistent variable naming.

---

## Code Quality Ratings

| Metric | Rating (1-10) | Evaluation Rationale |
| :--- | :---: | :--- |
| **Readability** | `4 / 10` | Cryptic variable names (`d`, `res`, `tmp`), nested conditional logic (4 levels deep), and absent docstrings made intent unclear. |
| **Performance** | `5 / 10` | Inefficient quadratic lookups (`O(n^2)`) using lists instead of hash sets for lookup verification. |
| **Maintainability** | `3 / 10` | High coupling, global state mutation, missing modular functions, and complete lack of unit test coverage. |

---

## Code Smells Identified
1. **Monolithic Function:** Single function extending over 90 lines handling HTTP requests, JSON parsing, validation, database insertion, and formatting.
2. **Generic Exception Swallowing:** Bare `except:` block suppressing error traces and returning `None`, masking underlying database connection timeouts.
3. **Magic Numbers and Hardcoded Configurations:** API URLs, timeout limits, and database connection strings embedded inline.
4. **SQL Injection Vulnerability:** Raw string formatting (`f"SELECT * FROM users WHERE id = {user_id}"`) used in query construction.

---

## Key Learnings (3rd Person Perspective)

### 1. The Value of Guard Clauses over Deep Nesting
Observed that replacing deeply nested `if/else` checks with early return guard clauses significantly simplifies reading order and keeps the main happy path at the root indentation level.

### 2. Parameterized Queries for Security and Performance
Learnt that raw string concatenation in SQL queries introduces critical security vulnerabilities and prevents database query execution plan caching. Enforcing parameterized query interfaces protects against injection and improves database execution speed.

### 3. Centralized Configuration Management
The review highlighted that hardcoding settings directly inside business logic hinders environment switching (testing vs. production). Moving configuration to environment variables or dedicated config objects makes the codebase configurable and secure.
