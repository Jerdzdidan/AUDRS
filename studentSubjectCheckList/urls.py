from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_checklist, name='student-subject-checklist'),
]