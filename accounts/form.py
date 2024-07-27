from django.contrib.auth.forms import UserCreationForm
from django import forms
from task_manager.models import (
    Worker,
    Position
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    position = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = Worker
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'position']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
