# Activity 1: Idiomatic Code Transformation Journal

## Overview
This journal documents three key learnings resulting from transforming non-idiomatic Python code into concise, idiomatic Python using modern features such as list comprehensions, dictionary comprehensions, tuple unpacking, and standard library built-ins.

---

## Key Learning 1: Leveraging Dictionary Direct Iteration and Comprehensions
The initial code manually extracted dictionary keys via `.keys()` and performed lookup operations inside an imperative `for` loop. The developer learned that Python dictionaries provide direct key-value iteration using `.items()`. Furthermore, combining dictionary comprehensions with inline expressions eliminates boilerplate dictionary initialization, key lookup, and manual insertion steps.

## Key Learning 2: Built-in Aggregations over Manual Accumulator Loops
The baseline function relied on explicit `total` and `count` accumulator variables modified inside conditional loops. The developer observed that leveraging Python's native `sum()` and `len()` functions over list comprehensions or generators drastically reduces code verbosity and eliminates potential off-by-one or initialization bugs.

## Key Learning 3: Explicit Type Annotations and Docstrings
The non-idiomatic version lacked type hints and explicit documentation, leaving function inputs and expected return types ambiguous. The developer recognized that incorporating type annotations (`dict[str, list[float]] -> dict[str, float]`) improves static analysis, IDE autocompletion, and readability for team members without incurring runtime overhead.
