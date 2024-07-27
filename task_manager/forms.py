from django import forms
from django.contrib.auth import get_user_model
from task_manager.models import (
    Task,
    Tag
)


class TaskCreationForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop("project_id", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "priority",
            "deadline",
            "type",
            "assignees",
            "tags",
        ]


class TaskUpdateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
        required=True,
    )

    class Meta:
        model = Task
        fields = [
            "description", "priority", "deadline", "assignees", "tags"
        ]


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=64,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by project name"}
        ),
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=64,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by task name"}
        ),
    )
    pending = forms.BooleanField(
        required=False,
        label="Pending",
        widget=forms.CheckboxInput(
            attrs={"class": "form-checkbox"}
        ),
    )
    assigned_to_user = forms.BooleanField(
        required=False,
        label="Assigned to me",
        widget=forms.CheckboxInput(
            attrs={"class": "form-checkbox"}
        ),
    )
