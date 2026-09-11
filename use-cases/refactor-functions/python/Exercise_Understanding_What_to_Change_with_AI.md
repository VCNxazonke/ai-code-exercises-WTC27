# Understanding What to Change with AI

## Scope Clarification

This document answers the three exercises in the source instructions. Exercises 1 and 3 use Java or JavaScript examples that are not part of this Python project. Exercise 2 is the applicable project task, so the implemented code answers that task directly.

## Exercise 1: Code Readability Improvement

**Question: What should be changed in the Java example?**

The Java class should use names such as `UserManager`, `users`, `databaseConnection`, `addUser`, `findUser`, `username`, `password`, and `email`. The database operation should also use parameterized SQL rather than string concatenation. No Java source was changed because this workspace contains the Python report exercise, not the Java example.

## Exercise 2: Function Refactoring

**Question: What should the Python function do?**

The sample function should process orders, update inventory, calculate prices and shipping, track revenue, and separate successful orders from errors.

**Question: How should it be broken into focused functions?**

The same decomposition principle was applied to this project's `generate_sales_report`: validation, filtering, summary calculation, grouping, detailed data, forecasting, chart preparation, and rendering now have separate helpers.

**Question: How does this compare with the assistant's approach?**

The assistant's approach agrees with the exercise: preserve the public entry point, move each responsibility behind a descriptive helper, and verify behavior with tests. The project-specific implementation was applied to the report generator rather than to the unrelated order sample.

## Exercise 3: Code Duplication Detection

**Question: What duplication appears in the JavaScript example?**

The code repeats loops for calculating averages and maximum values for age, income, and score. A reusable statistic helper could accept a field name or value extractor, while the returned structure would retain clear names.

**Question: Which approach is most readable for junior developers?**

A small helper with a descriptive name is more readable than a highly generic abstraction. The helper should make the extracted value explicit and keep the returned `average` and `highest` keys understandable.

## Final Reflection Question 1

**Which prompting strategy was most useful, and why?**

Function decomposition was most useful because it exposed the responsibilities inside the report generator and gave each responsibility a testable owner.

## Final Reflection Question 2

**What did the AI suggest that might not have been considered?**

It highlighted the value of strategy maps for report types and renderer selection, in addition to simple helper extraction.

## Final Reflection Question 3

**Was there any suggestion that was not accepted?**

The assistant did not add third-party PDF, Excel, or HTML libraries. Those functions were explicitly stubs in the starter project, and adding dependencies would exceed the refactoring exercise.

## Final Reflection Question 4

**How can these prompts be adapted to another codebase?**

The prompt should name the language, public API, business responsibilities, compatibility constraints, expected tests, and the specific quality issue being investigated.

## Final Reflection Question 5

**What safeguards should be used before applying AI-suggested refactoring?**

Run a baseline test suite, preserve public interfaces, make one focused change at a time, inspect the diff, run targeted tests after each change, and review edge cases such as empty data and invalid input.

## Project Verification

The final Python validation command was `python -m unittest test_sales_report`. All 11 tests passed and both Python files reported no diagnostics.
