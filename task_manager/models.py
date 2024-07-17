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
        Position, on_delete=models.CASCADE, null=True, related_name="workers"
    )

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name} "
            f"({self.position})"
        )


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return str(self.name)


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Urgent', 'Urgent'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES)
    created_at = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return (
            f"{self.name}: {self.type}"
            f"Description: {self.description}"
            f"Priority: {self.priority}"
            f"Deadline: {self.deadline}"
        )
