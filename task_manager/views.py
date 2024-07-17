from django.shortcuts import render
from django.views import generic
from .models import Project


# Create your views here.
class IndexListView(generic.ListView):
    model = Project
    template_name = "task_manager/index.html"
