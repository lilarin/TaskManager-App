from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Position, TaskType, Worker, Project, Tag, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name", "description", "priority",
        "created_at", "deadline", "type",
        "project", "is_completed", "display_assignees", "display_tags"
    ]
    list_filter = ["name", ]
    search_fields = ["name", ]

    def display_assignees(self, obj):
        return ", ".join([str(assignee) for assignee in obj.assignees.all()])

    display_assignees.short_description = 'Assignees'

    def display_tags(self, obj):
        return ", ".join([str(tag) for tag in obj.tags.all()])

    display_tags.short_description = 'Tags'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    list_filter = ["name", ]
    search_fields = ["name", ]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name", ]
    search_fields = ["name", ]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name", ]
    search_fields = ["name", ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name", ]
    search_fields = ["name", ]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional_info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Position", {"fields": ("position",)}),)
