from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.models import TaskType, Project, Task, Tag
from task_manager.forms import (
    TaskCreationForm,
    TaskUpdateForm,
    ProjectSearchForm,
    TaskSearchForm
)


class TaskFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.task_type = TaskType.objects.create(name="Test task type")
        self.project = Project.objects.create(
            name="Test project",
            description="Test project description"
        )
        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")

    def test_task_creation_form_valid_data(self):
        form = TaskCreationForm(data={
            'name': 'Test task',
            'description': 'Test description',
            'priority': 'High',
            'deadline': '2024-07-21',
            'type': self.task_type.id,
            'tags': [self.tag1.id, self.tag2.id],
            'assignees': [self.user.id],
        })
        self.assertTrue(form.is_valid())

    def test_task_creation_form_invalid_data(self):
        form = TaskCreationForm(data={})
        self.assertFalse(form.is_valid())

    def test_task_update_form_valid_data(self):
        task = Task.objects.create(
            name='Test task',
            description='Test description',
            priority='High',
            deadline='2024-07-21',
            type=self.task_type,
            project=self.project,
        )
        form = TaskUpdateForm(instance=task, data={
            'description': 'Updated description',
            'priority': 'Medium',
            'deadline': '2024-07-22',
            'tags': [self.tag1.id, self.tag2.id],
            'assignees': [self.user.id],
        })
        self.assertTrue(form.is_valid())

    def test_task_update_form_invalid_data(self):
        task = Task.objects.create(
            name='Test task',
            description='Test description',
            priority='High',
            deadline='2024-07-21',
            type=self.task_type,
            project=self.project,
        )
        form = TaskUpdateForm(instance=task, data={
            'deadline': '',
        })
        self.assertFalse(form.is_valid())

    def test_project_search_form(self):
        form = ProjectSearchForm(data={'name': 'Test'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'Test')

    def test_task_search_form(self):
        form = TaskSearchForm(data={
            'name': 'Test',
            'pending': False,
            'assigned_to_user': True,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'Test')
        self.assertFalse(form.cleaned_data['pending'])
        self.assertTrue(form.cleaned_data['assigned_to_user'])
