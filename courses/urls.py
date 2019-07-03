from django.urls import path

from .views import TechnologyListView, TechnologyDetailView, CourseListView, CourseDetailView, LessonDetailView

app_name = 'courses'

urlpatterns = [
    path('', TechnologyListView.as_view(), name='techs'),
    path('tech/<slug>', TechnologyDetailView.as_view(), name='tech-detail'),
    path('all/', CourseListView.as_view(), name='index'),
    path('course/<slug>', CourseDetailView.as_view(), name='detail'),
    path('course/<course_slug>/lesson/<lesson_slug>', LessonDetailView.as_view(), name='lesson-detail')
]