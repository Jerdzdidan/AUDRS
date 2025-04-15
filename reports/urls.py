from django.urls import path
from . import views

urlpatterns = [
    path('student-list/', views.student_list_report, name='student_list_report'),
    path('unregistered-student-list/', views.unregistered_student_list_report, name='unregistered_student_list_report'),
    path('pending-registration-list/', views.pending_registration_student_report, name='pending_registration_list_report'),
    path('completed-registration-list/', views.completed_registration_student_list_report, name='completed_student_list_report'),
]