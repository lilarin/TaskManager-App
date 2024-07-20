from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth import get_user_model
from task_manager.models import Project, Task, TaskType
from task_manager.forms import ProjectSearchForm, TaskSearchForm


def set_up_data():
    user = get_user_model().objects.create_user(
        username='testuser',
        password='password'
    )
    client = Client()
    client.login(username='testuser', password='password')
    project = Project.objects.create(
        name="Test project",
        description="Test project description"
    )
    task_type = TaskType.objects.create(name="Test task type")
    task = Task.objects.create(
        name="Test task",
        description="Test description",
        priority="High",
        deadline="2024-07-21",
        type=task_type,
        project=project
    )
    return client, task, project


class IndexListViewTests(TestCase):
    def setUp(self):
        self.client, _, _ = set_up_data()

    def test_index_view_status_code(self):
        response = self.client.get(reverse('task_manager:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse('task_manager:index'))
        self.assertTemplateUsed(response, 'task_manager/index.html')

    def test_index_view_context(self):
        response = self.client.get(reverse('task_manager:index'))
        self.assertIn('projects', response.context)
        self.assertIsInstance(response.context['search_form'], ProjectSearchForm)


class ProjectTaskListViewTests(TestCase):
    def setUp(self):
        self.client, _, self.project = set_up_data()

    def test_project_task_list_view_status_code(self):
        response = self.client.get(reverse('task_manager:project-task-list', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 200)

    def test_project_task_list_view_template(self):
        response = self.client.get(reverse('task_manager:project-task-list', kwargs={'pk': self.project.id}))
        self.assertTemplateUsed(response, 'task_manager/project_task_list.html')

    def test_project_task_list_view_context(self):
        response = self.client.get(reverse('task_manager:project-task-list', kwargs={'pk': self.project.id}))
        self.assertIn('tasks', response.context)
        self.assertIn('project', response.context)
        self.assertIsInstance(response.context['search_form'], TaskSearchForm)


class ProjectCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.client.login(username='testuser', password='password')

    def test_project_create_view_status_code(self):
        response = self.client.get(reverse('task_manager:project-create'))
        self.assertEqual(response.status_code, 200)

    def test_project_create_view_template(self):
        response = self.client.get(reverse('task_manager:project-create'))
        self.assertTemplateUsed(response, 'task_manager/project_form.html')

    def test_project_create(self):
        response = self.client.post(reverse('task_manager:project-create'), data={
            'name': 'New Project',
            'description': 'New project description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name='New Project').exists())


class TaskDetailViewTests(TestCase):
    def setUp(self):
        self.client, self.task, self.project = set_up_data()

    def test_task_detail_view_status_code(self):
        response = self.client.get(
            reverse('task_manager:task-detail', kwargs={'pk': self.task.id, 'project_id': self.project.id}))
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view_template(self):
        response = self.client.get(
            reverse('task_manager:task-detail', kwargs={'pk': self.task.id, 'project_id': self.project.id}))
        self.assertTemplateUsed(response, 'task_manager/task_detail.html')

    def test_task_detail_view_context(self):
        response = self.client.get(
            reverse('task_manager:task-detail', kwargs={'pk': self.task.id, 'project_id': self.project.id}))
        self.assertIn('task', response.context)
        self.assertEqual(response.context['task'], self.task)
