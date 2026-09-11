# Exercise 5: Part 3 - Advanced Prompting Techniques Practice

## 1. Contextual Ecosystem Comparison (Python `dataclasses` vs. Go Structs)
Python `@dataclass` auto-generates constructors (`__init__`), string representations (`__repr__`), and equality checks (`__eq__`). In Go, `struct` definitions hold named fields, while memory management (value passing vs. pointer references `*Struct`) is controlled explicitly at the call site.

## 2. Performance & Scaling Analysis
- **Memory Footprint:** Goroutines allocate ~2KB of initial stack memory compared to ~8MB for Python threads or heavy asyncio task overhead.
- **CPU Scaling:** Go compiled binaries execute native machine instructions directly without byte-code interpreter locks, allowing multi-core CPU scaling across concurrent routines.

## 3. Learning Through Teaching (Explanation of Go Channels)
Go channels behave like thread-safe FIFO queue pipes. Sender goroutines push data into channels (`ch <- value`), and receiver goroutines block until data is available (`val := <-ch`). Unbuffered channels synchronize both execution and data transfer simultaneously.

## 4. Tutor Persona Response Simulation
*AI Tutor Prompt Response:* "Instead of using global variables to pass state between routines, what Go concurrency primitive ensures synchronized access without race conditions?" -> Answer: Use channels or `sync.Mutex`.
