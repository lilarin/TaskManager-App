from django.urls import path
from task_manager.views import (
    IndexListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectTaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView
)


urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path(
        "projects/<int:pk>/tasks",
        ProjectTaskListView.as_view(),
        name="project-task-list",
    ),
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "projects/<int:pk>/tasks/create/",
        TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),
]

app_name = "task_manager"
