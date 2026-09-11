# Exercise 5: Part 4 - Reflection Answers

## Reflection Question 1: Which prompting strategies were most effective for your learning style?
Determined that combining the **Step-by-Step Breakdown** (comparing syntax side-by-side) with **Understanding Verification** was most effective. Requesting conceptual differences before code implementation prevented erroneous mental assumptions carried over from the source language.

## Reflection Question 2: What surprised you about the target language that wasn't immediately obvious?
Was surprised by Go's strict policy regarding unused variables and unused imports. While Python permits unused imports or variables, the Go compiler throws an explicit compilation error. This design choice guarantees clean codebases but requires adjusting developer workflow habits.

## Reflection Question 3: How did your mental models from your source language help or hinder learning?
Python's mental model of dynamic duck typing hindered early understanding of Go's compile-time interfaces. However, prior familiarity with REST APIs, middleware chains, and HTTP status codes accelerated learning framework implementation steps once the syntax boundary was crossed.

## Reflection Question 4: What would you do differently in your next learning session?
In future learning sessions, will focus earlier on writing unit tests using the target language's native test runner (`go test`) alongside feature learning, rather than delaying test authoring until after mini-project completion.

## Reflection Question 5: What gaps remain in your understanding of the target language?
Gaps remaining include advanced channel synchronization patterns (such as fan-in / fan-out pipeline processing), unsafe pointer casting (`unsafe.Pointer`), and Cgo interop calls.
