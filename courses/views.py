from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View


class CourseListView(ListView):
    pass


class CourseDetailView(DetailView):
    pass


class LessonDetailView(LoginRequiredMixin, View):
    pass
