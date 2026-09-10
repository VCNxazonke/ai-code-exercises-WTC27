import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from models import Task, TaskPriority, TaskStatus
from task_priority import (
    calculate_task_score,
    get_top_priority_tasks,
    sort_tasks_by_importance,
)


FIXED_NOW = datetime(2026, 1, 15, 12, 0, 0)


class TestCalculateTaskScore(unittest.TestCase):
    def score_at_fixed_time(self, task, current_user=None):
        with patch("task_priority.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = FIXED_NOW
            return calculate_task_score(task, current_user=current_user)

    def test_basic_score_uses_priority_and_recent_update(self):
        task = Task("Write documentation", priority=TaskPriority.MEDIUM)
        task.updated_at = FIXED_NOW - timedelta(days=2)

        self.assertEqual(self.score_at_fixed_time(task), 20)

    def test_due_date_bands_add_the_expected_score(self):
        expected_scores = {
            -1: 55,
            0: 40,
            2: 35,
            7: 30,
            8: 20,
        }

        for days_until_due, expected_score in expected_scores.items():
            with self.subTest(days_until_due=days_until_due):
                task = Task("Time-sensitive task", priority=TaskPriority.MEDIUM)
                task.due_date = FIXED_NOW + timedelta(days=days_until_due)
                task.updated_at = FIXED_NOW - timedelta(days=2)

                self.assertEqual(self.score_at_fixed_time(task), expected_score)

    def test_completed_and_review_tasks_are_deprioritized(self):
        completed = Task("Completed", priority=TaskPriority.MEDIUM)
        completed.status = TaskStatus.DONE
        completed.updated_at = FIXED_NOW - timedelta(days=2)
        in_review = Task("In review", priority=TaskPriority.MEDIUM)
        in_review.status = TaskStatus.REVIEW
        in_review.updated_at = FIXED_NOW - timedelta(days=2)

        self.assertEqual(self.score_at_fixed_time(completed), -30)
        self.assertEqual(self.score_at_fixed_time(in_review), 5)

    def test_priority_tags_add_eight_points(self):
        task = Task("Blocked task", priority=TaskPriority.MEDIUM, tags=["blocker"])
        task.updated_at = FIXED_NOW - timedelta(days=2)

        self.assertEqual(self.score_at_fixed_time(task), 28)

    def test_recent_update_adds_five_points_but_two_days_does_not(self):
        recent = Task("Recently changed", priority=TaskPriority.LOW)
        recent.updated_at = FIXED_NOW - timedelta(hours=23)
        older = Task("Older change", priority=TaskPriority.LOW)
        older.updated_at = FIXED_NOW - timedelta(days=2)

        self.assertEqual(self.score_at_fixed_time(recent), 15)
        self.assertEqual(self.score_at_fixed_time(older), 10)


class TestAssignedUserScoreBoost(unittest.TestCase):
    def test_task_assigned_to_current_user_gets_twelve_point_boost(self):
        task = Task("Prepare release notes", priority=TaskPriority.HIGH)
        task.assigned_to = "alice"
        task.updated_at = FIXED_NOW - timedelta(days=2)

        with patch("task_priority.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = FIXED_NOW
            score_for_other_user = calculate_task_score(task, current_user="bob")
            score_for_current_user = calculate_task_score(task, current_user="alice")

        self.assertEqual(score_for_current_user - score_for_other_user, 12)


class TestPriorityWorkflow(unittest.TestCase):
    def make_task(self, title, priority, due_date=None, assigned_to=None):
        task = Task(title, priority=priority, due_date=due_date, assigned_to=assigned_to)
        task.updated_at = FIXED_NOW - timedelta(days=2)
        return task

    def test_sort_and_top_priority_use_the_same_scoring_workflow(self):
        low = self.make_task("Low priority", TaskPriority.LOW)
        due_soon = self.make_task(
            "Due soon", TaskPriority.MEDIUM, FIXED_NOW + timedelta(days=1)
        )
        assigned = self.make_task(
            "Assigned to Alice", TaskPriority.HIGH, assigned_to="alice"
        )
        tasks = [low, due_soon, assigned]

        with patch("task_priority.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = FIXED_NOW
            sorted_tasks = sort_tasks_by_importance(tasks, current_user="alice")
            top_tasks = get_top_priority_tasks(tasks, limit=2, current_user="alice")

        self.assertEqual([task.title for task in sorted_tasks], [
            "Assigned to Alice",
            "Due soon",
            "Low priority",
        ])
        self.assertEqual(top_tasks, sorted_tasks[:2])

    def test_top_priority_limit_and_empty_input_are_respected(self):
        self.assertEqual(get_top_priority_tasks([], limit=5), [])
        task = self.make_task("Any task", TaskPriority.LOW)
        self.assertEqual(get_top_priority_tasks([task], limit=0), [])


if __name__ == "__main__":
    unittest.main()
