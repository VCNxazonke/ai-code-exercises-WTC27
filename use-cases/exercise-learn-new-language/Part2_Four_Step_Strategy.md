# Exercise 5: Part 2 - Four-Step Prompting Strategy Application

This document applies the four-step prompting strategy for learning Go coming from Python.

---

## Step 1: Conceptual Understanding
**Key Philosophical Differences:**
- **Explicit vs. Implicit Execution:** Python heavily utilizes implicit dynamic magic (duck typing, monkey patching, decorators). Go prioritizes absolute code visibility, explicit error returns (`if err != nil`), and compile-time verification.
- **Concurrency Paradigm:** Python relies on `asyncio` event loops or multi-threading with Global Interpreter Lock (GIL) constraints. Go uses Communicating Sequential Processes (CSP) with native OS-thread scheduled goroutines.

## Step 2: Step-by-Step Breakdown (Error Handling)
**Implementation Breakdown:**
- Python uses `try/except` stack unwinding exceptions.
- Go treats errors as explicit values implementing the `error` interface (`type error interface { Error() string }`). Functions returning potential failures include error as the final return value.

## Step 3: Guided Implementation
**Syntactic Example:**
```go
package main

import (
    "errors"
    "fmt"
)

func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("cannot divide by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 2)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)
}
```

## Step 4: Understanding Verification
The implementation above verifies that error conditions are handled immediately at the call site before proceeding, enforcing defensive programming and preventing unhandled runtime exceptions.
