from django.test import TestCase
from task_manager.models import (
    Task,
    TaskType,
    Project,
    Tag
)


class TaskModelTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Test task type")
        self.project = Project.objects.create(
            name="Test project", description="Test project description"
        )
        self.task = Task.objects.create(
            name="Test task",
            description="Test task description",
            priority="Low",
            deadline="2024-07-20",
            type=self.task_type,
            project=self.project,
        )

    def test_correct_data(self):
        self.assertEqual(self.task.name, "Test task")
        self.assertFalse(self.task.is_completed)
        self.assertEqual(len(self.task.assignees.all()), 0)
        self.assertEqual(len(self.task.tags.all()), 0)

    def test_task_tags(self):
        tag1 = Tag.objects.create(name="Urgent")
        tag2 = Tag.objects.create(name="Bug")
        self.task.tags.add(tag1, tag2)
        self.assertEqual(self.task.tags.count(), 2)
        self.assertIn(tag1, self.task.tags.all())
        self.assertIn(tag2, self.task.tags.all())

    def test_unique_task_name(self):
        with self.assertRaises(Exception):
            Task.objects.create(
                name="Test task",
                description="Another task description",
                priority="Medium",
                deadline="2024-07-21",
                type=self.task_type,
                project=self.project,
            )

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test project")
