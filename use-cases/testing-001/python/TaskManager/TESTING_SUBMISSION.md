# Testing Exercise Submission

This submission follows `Exercise_Using AI_to_Help_with_Testing.txt`. The implementation names use Python snake_case: `calculate_task_score`, `sort_tasks_by_importance`, and `get_top_priority_tasks`.

## Part 1: Understanding What to Test

### Exercise 1.1: Behavior Analysis

The score is built from independent, observable task behaviors:

1. Base priority contributes 10, 20, 40, or 60 points for low, medium, high, or urgent.
2. Due dates add 35 for overdue, 20 for today, 15 for the next two days, and 10 for the next week.
3. Completed tasks lose 50 points; tasks in review lose 15 points.
4. `blocker`, `critical`, and `urgent` tags add 8 points.
5. An update less than one day old adds 5 points.
6. A task assigned to the supplied current user adds 12 points.
7. Missing due dates and non-matching users do not add points.

The highest-value first test is the basic priority calculation because it establishes the score baseline used by every later behavior. The edge cases are boundary dates (overdue, today, two days, seven days, and eight days), status deductions, empty tags, no due date, and the exact one-day elapsed-time boundary.

### Exercise 1.2: Test Planning

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

## Part 2: Improving a Single Test

### Exercise 2.1: Writing Your First Test

The simple test idea was to calculate one score and assert a number. The improved test, `test_basic_score_uses_priority_and_recent_update`, makes the purpose explicit by fixing the clock, setting an older update time, and asserting the exact base score. This verifies public behavior rather than the internal `priority_weights` dictionary.

The suite also improves assertion precision by checking exact deltas for the +12 assignment feature and exact scores for every due-date band.

### Exercise 2.2: Learning From Examples

For due-date behavior, a good test controls the current time and places the due date at each meaningful boundary. `test_due_date_bands_add_the_expected_score` uses subtests for overdue, today, two days, seven days, and eight days. Its assertions verify the externally visible score, not how the date arithmetic is implemented.

## Part 3: Test-Driven Development Practice

### Exercise 3.1: TDD for a New Feature

The first test was written before the implementation:

- `test_task_assigned_to_current_user_gets_twelve_point_boost` first failed because the function did not accept `current_user`.
- The minimal implementation added an optional `current_user`, an optional `Task.assigned_to`, and the +12 score rule.
- The same test then passed.
- Sorting and top-N were updated to pass the user context through without breaking existing callers.

The model and storage path also preserve `assigned_to`, so the feature is not lost when tasks are serialized and loaded.

### Exercise 3.2: TDD for a Bug Fix

`test_recent_update_adds_five_points_but_two_days_does_not` is the regression test for the days-since-update bug. It verifies that a 23-hour-old update receives the +5 boost while an update two days old does not. The current starter implementation already uses `timedelta.days`; therefore no unnecessary source rewrite was made. The test locks the corrected `.days` behavior against future regression.

## Part 4: Integration Testing

### Exercise 4.1: Testing the Full Workflow

`test_sort_and_top_priority_use_the_same_scoring_workflow` creates low-priority, soon-due, and current-user-assigned tasks. It passes them through `sort_tasks_by_importance` and `get_top_priority_tasks`, then verifies both the complete order and the top-two prefix. This confirms that the assignment boost affects the combined workflow and that top-N delegates to the same ordering behavior.

Boundary coverage for empty input and a zero limit is in `test_top_priority_limit_and_empty_input_are_respected`.

## Reflection

The exercise showed that good tests begin with observable behavior and explicit boundaries, not with the implementation's internal structure. Fixing the clock made date tests repeatable, and comparing the assigned-user score with the non-matching-user score made the new requirement precise. The TDD cycle also exposed the API change before implementation, while the integration test checked that the new score factor remained effective after sorting and limiting.

## Verification

Run from this folder:

```text
python -m unittest -v test_task_priority
```

The completed suite contains 8 tests covering unit behavior, edge cases, TDD regression coverage, and integration behavior.
