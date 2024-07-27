from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.forms import (
    TaskCreationForm,
    ProjectSearchForm,
    TaskSearchForm,
)
from task_manager.models import (
    TaskType,
    Project,
    Tag
)


class TaskFormTests(TestCase):
    def get_creation_data(self):
        return {
            "name": "Test task",
            "description": "Test description",
            "priority": "High",
            "deadline": "2024-07-21",
            "project": self.project,
            "type": self.task_type,
            "tags": [self.tag1, self.tag2],
        }

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.task_type = TaskType.objects.create(
            name="Test task type"
        )
        self.project = Project.objects.create(
            name="Test project",
            description="Test project description"
        )
        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")

    def test_task_creation_form_valid_data(self):
        form = TaskCreationForm(
            data=self.get_creation_data()
        )
        self.assertTrue(form.is_valid())

    def test_task_creation_form_invalid_data(self):
        form = TaskCreationForm(data={})
        self.assertFalse(form.is_valid())

    def test_project_search_form(self):
        form = ProjectSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

    def test_task_search_form(self):
        form = TaskSearchForm(
            data={
                "name": "Test",
                "pending": False,
                "assigned_to_user": True,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")
        self.assertFalse(form.cleaned_data["pending"])
        self.assertTrue(form.cleaned_data["assigned_to_user"])
