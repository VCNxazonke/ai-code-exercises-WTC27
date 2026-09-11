# Personalized Python Style & Best Practices Guide

## 1. Code Layout & Formatting
- **PEP 8 Compliance:** Use 4 spaces per indentation level. Maximum line length is capped at 88 characters (Black formatter standard).
- **Import Ordering:** Group imports in three sections separated by single blank lines: standard library imports, third-party library imports, and local project imports.

## 2. Naming Conventions
- **Variables & Functions:** Use `snake_case` (e.g., `calculate_user_balance`).
- **Classes:** Use `PascalCase` (e.g., `TaskRepository`).
- **Constants:** Use `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_ATTEMPTS`).
- **Private Attributes:** Prefix internal helper functions or private attributes with a single underscore (e.g., `_format_internal_date`).

## 3. Type Annotations & Static Analysis
- Annotate parameters and return types for all public module functions and class methods.
- Use `typing` generic aliases (`list[int]`, `dict[str, Any]`, `Optional[str]`).
- Run `mypy` or static analysis before code review submission.

## 4. Error & Resource Handling
- Always use `with` statements (context managers) when working with files, network connections, or database locks.
- Raise specific error classes (`ValueError`, `KeyError`, custom HTTP exceptions) rather than generic `Exception`.
