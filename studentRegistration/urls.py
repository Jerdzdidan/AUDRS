from django.urls import path
from . import views

urlpatterns = [
    path('open-registration/', views.open_registration_custom, name='open_registration_custom'),
    path('registration-calendar/', views.registration_calendar, name='registration_calendar'),
    path('registration-form/', views.student_registration_form, name='student_registration_form'),
    path('registration-queue/', views.student_registration_queue, name='student_registration_queue'),
    path('registration-detail-student/<str:student_id>/', views.student_registration_detail_for_student, name='student_registration_detail_for_student'),
    path('registration-edit/', views.student_registration_edit, name='student_registration_edit'),

    path('download-registration-image/<int:registration_id>/', views.download_registration_image, name='download_registration_image'),
    
    path('registration-detail/<str:student_id>/', views.student_registration_detail, name='student_registration_detail'),
    path('finalize-registration/<str:student_id>/', views.finalize_registration, name='finalize_registration'),
]