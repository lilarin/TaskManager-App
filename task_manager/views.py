from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from task_manager.forms import (
    ProjectSearchForm,
    TaskSearchForm,
    TaskCreationForm,
    TaskUpdateForm,
)
from task_manager.models import (
    Project,
    Task,
    Worker
)


class IndexListView(generic.ListView):
    model = Project
    template_name = "task_manager/index.html"
    context_object_name = "projects"
    search_form_class = ProjectSearchForm
    search_field = "name"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get(self.search_field, "")
        context["search_form"] = self.search_form_class(
            initial={self.search_field: search_value}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.search_form_class(self.request.GET)
        if form.is_valid():
            search_value = form.cleaned_data[self.search_field]
            return queryset.filter(**{f"{self.search_field}__icontains": search_value})
        return queryset


class ProjectTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/project_task_list.html"
    context_object_name = "tasks"
    search_form_class = TaskSearchForm
    search_field = "name"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get(self.search_field, "")
        context["project"] = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        context["search_form"] = self.search_form_class(
            initial={
                self.search_field: search_value,
                "pending": self.request.GET.get("pending") == "on",
                "assigned_to_user": self.request.GET.get("assigned_to_user") == "on",
            }
        )
        return context

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        queryset = super().get_queryset().filter(project_id=project.id)
        form = self.search_form_class(self.request.GET)
        if form.is_valid():
            search_value = form.cleaned_data.get(self.search_field, "")
            if search_value:
                queryset = queryset.filter(
                    **{f"{self.search_field}__icontains": search_value}
                )
            if form.cleaned_data.get("pending"):
                queryset = queryset.filter(is_completed=False)
            assigned = form.cleaned_data.get("assigned_to_user")
            if assigned:
                user = Worker.objects.get(id=self.request.user.id)
                queryset = queryset.filter(assignees=user)
        return queryset


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:index")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs.get("pk")
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project_id"] = self.kwargs.get("project_id")
        return kwargs

    def form_valid(self, form):
        form.instance.project_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:project-task-list", kwargs={"pk": self.kwargs["pk"]}
        )


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:project-task-list", kwargs={"pk": self.object.project_id}
        )


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:project-task-list", kwargs={"pk": self.object.project_id}
        )


@login_required()
def toggle_task_status(request: HttpRequest, project_id: int, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return HttpResponseRedirect(
        reverse_lazy(
            "task_manager:task-detail", kwargs={"project_id": project_id, "pk": pk}
        )
    )
