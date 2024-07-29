from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from accounts.form import UserRegisterForm


class RegisterView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("task_manager:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response
