from django.urls import path
from . import views

urlpatterns = [
    path('subject-list/', views.subject_list_department, name='subject-management-list'),
    path('subject-approval-queue/', views.subject_approval_queue, name='subject-management-approval-queue'),
    path('create-subject/', views.create_subject, name="subject-management-create-subject"),
    path('update-subject/<int:subject_id>/', views.update_subject, name="subject-management-update-subject"),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name="subject-management-delete-subject"),
]