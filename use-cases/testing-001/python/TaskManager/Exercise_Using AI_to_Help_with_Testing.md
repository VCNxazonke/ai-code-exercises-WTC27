########################################################
INSTRUCTIONS TO AI AGENT: DO NOT TOUCH THIS FILE PLEASE
RATHER CREATE A NEW FILE IF NEED BE
########################################################

Exercise: Using AI to Help with Testing

This submission follows implementation names using Python snake_case: `calculate_task_score`, `sort_tasks_by_importance`, and `get_top_priority_tasks`.

Part 1: Understanding What to Test
Exercise 1.1: Behavior Analysis

1. Examined the calculateTaskScore function from chosen language implementation.

2. Used the following prompt with an AI assistant to help analyze what to test:

I'm learning how to test this function, and I want to understand what behaviors I should test:[calculateTaskScore function]Rather than generating tests for me, please:Ask me questions about what I think this function doesAfter I answer, help identify any behaviors I missedAsk me what edge cases I think should be testedHelp me identify additional edge cases I didn't think ofAsk me which test I should write first and why
3. Engaged in the conversation with the AI, answering its questions about the function's behavior.
4. Based on the conversation, created a list of at least 5 test cases that should be written, including any edge cases identified.
The score is built from independent, observable task behaviors:

4.1. Base priority contributes 10, 20, 40, or 60 points for low, medium, high, or urgent.
4.2. Due dates add 35 for overdue, 20 for today, 15 for the next two days, and 10 for the next week.
4.3. Completed tasks lose 50 points; tasks in review lose 15 points.
4.4. `blocker`, `critical`, and `urgent` tags add 8 points.
4.5. An update less than one day old adds 5 points.
4.6. A task assigned to the supplied current user adds 12 points.
4.7. Missing due dates and non-matching users do not add points.

The highest-value first test is the basic priority calculation because it establishes the score baseline used by every later behavior. The edge cases are boundary dates (overdue, today, two days, seven days, and eight days), status deductions, empty tags, no due date, and the exact one-day elapsed-time boundary.
______________________________________________________
Exercise 1.2: Test Planning
______________________________________________________
1. Focused on the entire set of functions: calculateTaskScore, sortTasksByImportance, and getTopPriorityTasks.
2. Used this prompt to help plan your testing approach:I'm learning to write tests for these related functions:[Project folder]Instead of writing tests for me, please:Help me create a testing plan by asking me questionsFor each behavior I identify, ask me how I would test itIf I miss something important, give me hints rather than answersFor each edge case we identify, ask me what I expect to happenHelp me create a checklist of tests I should write, organized by priority
3. Created a structured test plan document based on your conversation, including:
o Priority of test cases
o Types of tests needed (unit, integration)
o Test dependencies
o Expected outcomes for each test

### Exercise 3.1: Test Planning

| Priority | Behavior | Test type | Dependency | Expected outcome |
| --- | --- | --- | --- | --- |
| P0 | Base priority score | Unit | `Task`, `TaskPriority` | Correct base score for each priority |
| P0 | Assigned current user receives +12 | Unit/TDD | `Task.assigned_to` and `current_user` | Matching user raises score by exactly 12 |
| P0 | Due-date score bands | Unit | Controlled current time | Each boundary uses the documented addition |
| P0 | Sorting uses calculated score | Integration | Score function | Highest score appears first |
| P0 | Top-N returns sorted prefix | Integration | Sorting function | Limit is respected and order is preserved |
| P1 | Completed/review deductions | Unit | `TaskStatus` | Correct deductions are applied |
| P1 | Priority tags | Unit | Task tags | One qualifying tag adds 8 |
| P1 | Days since update | Regression | Controlled current time | Less than one day adds 5; two days does not |
| P2 | Empty input and zero limit | Unit/integration | No external dependency | Empty list or zero limit returns an empty list |

Tests use only the Python standard library. `unittest.mock.patch` fixes `datetime.now()` so date tests are deterministic.
______________________________________________________
Part 2: Improving a Single Test
____________________________________________________
______________________________________________________
Exercise 2.1: Writing Your First Test
______________________________________________________
1. Wrote a basic test for the calculateTaskScore function, intentionally made it simple (just test the basic functionality).
2. Used this prompt to improve your test:I wrote this test for the following function:Function:[ calculateTaskScore function]My test:[in project folder]Instead of rewriting it for me, please:Ask me questions about what my test is trying to verifyHelp me identify if my test is checking behavior or implementation detailsSuggest how I could make the test's purpose clearerAsk me what edge cases my test might be missingGuide me in improving my assertions to be more precise
3. Based on the feedback, rewrite your test to make it more robust and clearer.
### Exercise 2.1: Writing Your First Test

The simple test idea was to calculate one score and assert a number. The improved test, `test_basic_score_uses_priority_and_recent_update`, makes the purpose explicit by fixing the clock, setting an older update time, and asserting the exact base score. This verifies public behavior rather than the internal `priority_weights` dictionary.

The suite also improves assertion precision by checking exact deltas for the +12 assignment feature and exact scores for every due-date band.

______________________________________________________
Exercise 2.2: Learning From Examples
______________________________________________________
1. Chose another aspect of the calculateTaskScore function to test (e.g., due date calculations).
2. Used this prompt:I'm trying to understand how to better test the due date calculation portion of this function:[Paste calculateTaskScore function]I'm thinking of writing a test like this (pseudocode):[Write a rough outline/pseudocode of test idea]Please:Explain the principles of a good test for this specific functionalityShow me ONE example of a better test with comments explaining why it's betterAsk me questions about how I would improve my approach based on this exampleChallenge me to identify what edge cases I should addGuide me in writing more precise assertions
3. Wrote a comprehensive test for the due date calculation functionality based on conversation.
### Exercise 2.2: Learning From Examples

For due-date behavior, a good test controls the current time and places the due date at each meaningful boundary. `test_due_date_bands_add_the_expected_score` uses subtests for overdue, today, two days, seven days, and eight days. Its assertions verify the externally visible score, not how the date arithmetic is implemented.
____________________________________________________
Part 3: Test-Driven Development Practice
____________________________________________________
Exercise 3.1: TDD for a New Feature
1. Need to add a new feature to the task priority system: tasks assigned to the current user should get a score boost of +12.
2. Used this prompt before writing any code:I want to practice Test-Driven Development to add a new feature:Tasks assigned to the current user should get a score boost of +12.Here's the current function:[Paste calculateTaskScore function]Instead of writing code and tests for me, please:Ask me what I think the first test should be and whyGive me feedback on my proposed testAfter I write the test, ask me what minimal code would make it passOnce I've implemented the code, guide me on what test to add nextHelp me understand when it's time to refactor vs. add new functionality
3. Followed the TDD process:
o Wrote a failing test for the new feature
o Implemented the minimal code to make it pass
o Refactored if necessary
o Wrote the next test where needed

### Exercise 3.1: TDD for a New Feature

The first test was written before the implementation:

- `test_task_assigned_to_current_user_gets_twelve_point_boost` first failed because the function did not accept `current_user`.
- The minimal implementation added an optional `current_user`, an optional `Task.assigned_to`, and the +12 score rule.
- The same test then passed.
- Sorting and top-N were updated to pass the user context through without breaking existing callers.

The model and storage path also preserve `assigned_to`, so the feature is not lost when tasks are serialized and loaded.

______________________________________________________
Exercise 3.2: TDD for Bug Fix
______________________________________________________
1. There's a bug in the existing code: the calculation for "days since update" is incorrect and should be using .days instead of dividing by milliseconds.
2. Used this prompt:I want to practice TDD to fix a bug:The calculation for "days since update" isn't working correctly.Here's the current function:[Paste calculateTaskScore function]Please:Ask me what test I would write to reproduce the bugHelp me understand if my test actually demonstrates the bugGuide me in implementing a minimal fixAsk me if there are any other tests I should add to prevent regression
3. Wrote a test that demonstrates the bug, then fixed the code to make the test pass.

### Exercise 3.2: TDD for a Bug Fix

`test_recent_update_adds_five_points_but_two_days_does_not` is the regression test for the days-since-update bug. It verifies that a 23-hour-old update receives the +5 boost while an update two days old does not. The current starter implementation already uses `timedelta.days`; therefore no unnecessary source rewrite was made. The test locks the corrected `.days` behavior against future regression.

______________________________________________________
Part 4: Integration Testing

Exercise 4.1: Testing the Full Workflow
______________________________________________________

1. Thought about how to test the three functions working together: calculateTaskScore, sortTasksByImportance, and getTopPriorityTasks.
2. Used this prompt:I want to create an integration test for the task priority workflow:[Paste all three functions]Rather than writing the test for me, please:Ask me what scenarios an integration test should verifyGuide me in designing test data that would exercise the entire workflowHelp me understand what assertions would verify the correct behaviorAsk me how I would structure the test to make it readable and maintainable
3. Wrote an integration test that verifies the three functions work correctly together.

### Exercise 4.1: Testing the Full Workflow

`test_sort_and_top_priority_use_the_same_scoring_workflow` creates low-priority, soon-due, and current-user-assigned tasks. It passes them through `sort_tasks_by_importance` and `get_top_priority_tasks`, then verifies both the complete order and the top-two prefix. This confirms that the assignment boost affects the combined workflow and that top-N delegates to the same ordering behavior.

Boundary coverage for empty input and a zero limit is in `test_top_priority_limit_and_empty_input_are_respected`.

***Submission***
After completing all parts of this exercise, prepared this short document that includes:
i. test plan from Part 1
ii. improved unit tests from Part 2
iii. TDD implementation and tests from Part 3
iv. integration test from Part 4
v. A reflection on what was learnt about testing through this exercise

## Reflection
The exercise showed that good tests begin with observable behavior and explicit boundaries, not with the implementation's internal structure. Fixing the clock made date tests repeatable, and comparing the assigned-user score with the non-matching-user score made the new requirement precise. The TDD cycle also exposed the API change before implementation, while the integration test checked that the new score factor remained effective after sorting and limiting.

## Verification
Run from this folder:

```text
python -m unittest -v test_task_priority
```

The completed suite contains 8 tests covering unit behavior, edge cases, TDD regression coverage, and integration behavior.


Submitted this to the facilitator through repository, and to discuss this in the group discussion.