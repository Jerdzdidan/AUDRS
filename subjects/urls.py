from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_management_list, name='subject-management-list'),
]