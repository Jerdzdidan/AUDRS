from django.urls import path
from . import views

urlpatterns = [
    path('studentlist/', views.student_list_for_checklist, name='student-subject-studentlist'),
    path('checklist/<str:student_id>/', views.subject_checklist, name='student-subject-checklist'),
]