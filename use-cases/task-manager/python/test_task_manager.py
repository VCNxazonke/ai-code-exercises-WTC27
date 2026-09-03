# task_manager/test_task_manager.py
import unittest
import os
import csv
from datetime import datetime, timedelta
from .models import Task, TaskPriority, TaskStatus
from .storage import TaskStorage
from .app import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.test_storage_path = "test_tasks.json"
        self.test_csv_path = "test_export.csv"
        if os.path.exists(self.test_storage_path):
            os.remove(self.test_storage_path)
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)
        self.manager = TaskManager(storage_path=self.test_storage_path)

    def tearDown(self):
        if os.path.exists(self.test_storage_path):
            os.remove(self.test_storage_path)
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)

    def test_create_and_get_task(self):
        task_id = self.manager.create_task("Test Task", "Description", priority_value=3, due_date_str="2026-12-31", tags=["test", "unit"])
        self.assertIsNotNone(task_id)
        task = self.manager.get_task_details(task_id)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        self.assertEqual(task.tags, ["test", "unit"])

    def test_overdue_and_auto_abandonment_rules(self):
        # 1. Normal task, overdue 10 days, MEDIUM priority -> should be abandoned
        task1 = Task("Old Medium Task", priority=TaskPriority.MEDIUM, due_date=datetime.now() - timedelta(days=10))
        self.assertTrue(task1.is_overdue())
        self.assertTrue(task1.should_be_abandoned(days_overdue=7))

        # 2. High priority task, overdue 10 days -> exempt from abandonment
        task2 = Task("Old High Task", priority=TaskPriority.HIGH, due_date=datetime.now() - timedelta(days=10))
        self.assertTrue(task2.is_overdue())
        self.assertFalse(task2.should_be_abandoned(days_overdue=7))

        # 3. Task overdue only 3 days -> not yet abandoned
        task3 = Task("Recent Overdue Task", priority=TaskPriority.LOW, due_date=datetime.now() - timedelta(days=3))
        self.assertTrue(task3.is_overdue())
        self.assertFalse(task3.should_be_abandoned(days_overdue=7))

        # Save tasks to manager and process abandonment
        self.manager.storage.add_task(task1)
        self.manager.storage.add_task(task2)
        self.manager.storage.add_task(task3)

        count = self.manager.process_abandoned_tasks(days_overdue=7)
        self.assertEqual(count, 1)
        self.assertEqual(self.manager.get_task_details(task1.id).status, TaskStatus.ABANDONED)
        self.assertEqual(self.manager.get_task_details(task2.id).status, TaskStatus.TODO)
        self.assertEqual(self.manager.get_task_details(task3.id).status, TaskStatus.TODO)

    def test_csv_export(self):
        self.manager.create_task("Export Task 1", "Desc 1", priority_value=1)
        self.manager.create_task("Export Task 2", "Desc 2", priority_value=4)

        success = self.manager.export_tasks(self.test_csv_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.test_csv_path))

        with open(self.test_csv_path, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 2)
            self.assertEqual(reader[0]['title'], "Export Task 1")

if __name__ == '__main__':
    unittest.main()
