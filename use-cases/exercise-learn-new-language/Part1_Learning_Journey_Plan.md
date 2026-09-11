# Exercise 5: Part 1 - Learning Journey Plan (Python to Go API Development)

## Overview
This plan establishes a structured 4-phase learning journey for transitioning from Python to **Go (Golang)** for high-throughput microservice API development.

---

## Learning Phases

### Phase 1: Core Syntax & Memory Model Basics
- **Prerequisites:** Python functions, primitive types, basic data structures.
- **Steps:**
  1. Learn Go static typing, variable declarations (`var`, `:=`), and explicit error handling (`if err != nil`).
  2. Master value types vs. pointers (`*`, `&`) and memory allocations (`make`, `new`).
  3. Explore Go struct definitions, composition over inheritance, and methods with value/pointer receivers.
  4. Understand arrays, slices, slice capacity, and hash maps (`map[string]T`).
- **Verification:** Implement a CLI calculator handling string parsing, pointer mutations, and custom error structs.

### Phase 2: Interfaces & Idiomatic Structural Typing
- **Prerequisites:** Completion of Phase 1; understanding Python Duck Typing and Abstract Base Classes.
- **Steps:**
  1. Study implicit interface satisfaction in Go (no `implements` keyword required).
  2. Implement common standard library interfaces (`io.Reader`, `io.Writer`, `fmt.Stringer`, `error`).
  3. Master type assertions (`val, ok := i.(T)`) and type switches (`switch v := i.(type)`).
- **Verification:** Write a custom JSON log formatter component satisfying the `io.Writer` interface.

### Phase 3: Concurrency with Goroutines and Channels
- **Prerequisites:** Phase 2; familiarity with async/await and thread concurrency concepts.
- **Steps:**
  1. Learn lightweight goroutine spawning (`go func()`).
  2. Master buffered and unbuffered channels (`chan T`) for message passing.
  3. Implement worker pool concurrency patterns using `select` statements and `sync.WaitGroup`.
- **Verification:** Build a concurrent HTTP link checker processing 50 URLs in parallel with worker pools.

### Phase 4: Production Web Service Architecture
- **Prerequisites:** Phase 3; experience with REST API concepts.
- **Steps:**
  1. Build HTTP handlers using standard `net/http` and `chi` router.
  2. Implement middleware chains for request logging, JWT validation, and recovery.
  3. Package and build standalone binary executables.
- **Verification:** Deploy a production-ready REST API microservice with unit tests and benchmarking.
