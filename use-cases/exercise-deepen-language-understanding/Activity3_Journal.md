# Activity 3: Advanced Language Feature Journal - Python Decorators

## Overview
This journal details three key learnings resulting from exploring Python decorators, higher-order functions, and closure mechanisms.

---

## Key Learning 1: Metadata Preservation with `functools.wraps`
The developer discovered that wrapping a target function inside a decorator without `@functools.wraps(func)` overwrites the original function's `__name__` and `__doc__` attributes with those of the inner wrapper. Preserving metadata is critical for debugging, logging, and documentation tools.

## Key Learning 2: Stacking and Execution Order of Multiple Decorators
The developer learned that decorators are applied from bottom to top (inside out). In `@log_execution_time` placed above `@validate_positive_args`, the validation decorator runs first inside the wrapper stack. If validation fails, execution short-circuits before performance logging begins.

## Key Learning 3: Practical Separation of Cross-Cutting Concerns
The exercise demonstrated that decorators effectively decouple core business logic (such as financial compound interest calculation) from cross-cutting concerns (such as execution timing, argument validation, access control, and auditing).
