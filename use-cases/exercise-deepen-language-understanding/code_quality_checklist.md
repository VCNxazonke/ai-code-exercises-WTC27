# Python Code Quality Review Checklist

This checklist acts as a standard review tool for pull requests and code inspections.

## 1. Structure & Naming
- [ ] Are variable and function names descriptive, intention-revealing, and PEP 8 compliant?
- [ ] Are functions kept small (under 30 lines) with a single responsibility?
- [ ] Is deep nesting avoided by using early returns and guard clauses?
- [ ] Are magic numbers and hardcoded values replaced with named constants or configuration objects?

## 2. Type Safety & Documentation
- [ ] Do function signatures include explicit type hints for parameters and return types?
- [ ] Do public classes and methods have descriptive docstrings explaining intent and arguments?

## 3. Error Handling & Security
- [ ] Are exceptions caught specifically (avoiding bare `except:` or broad `except Exception:`)?
- [ ] Is input validation performed at system boundaries?
- [ ] Are SQL queries strictly parameterized to prevent injection vulnerabilities?
- [ ] Are secrets, API keys, and database credentials excluded from source code and managed via environment variables?

## 4. Performance & Efficiency
- [ ] Are appropriate data structures used (e.g., `set` for lookup operations instead of `list`)?
- [ ] Are resource handles (files, database sessions, HTTP connections) properly closed using context managers (`with` statements)?
- [ ] Is duplicate logic extracted into reusable helper functions?
