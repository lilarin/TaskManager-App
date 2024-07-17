from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return str(self.position)


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Urgent', 'Urgent'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return (
            f"{self.name}: {self.task_type}"
            f"Description: ({self.description})"
            f"Priority: {self.priority}"
            f"Deadline: {self.deadline}"
        )


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return f"{self.name} ({self.description})"
