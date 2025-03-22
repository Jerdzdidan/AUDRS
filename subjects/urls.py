from django.urls import path
from . import views

urlpatterns = [
    path('subject-list/', views.subject_list_department, name='subject-management-list'),
]