from django.urls import path
from task_manager.views import (
    IndexListView
)


urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
]

app_name = "task_manager"
