from django.contrib import admin
from .models import StudentRegistration, RegistrationWindow

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'student', 
        'preferred_section', 
        'preferred_time_start', 
        'preferred_time_end', 
        'registration_date', 
        'completed', 
        'submitted'
    )
    list_filter = ('preferred_section', 'completed', 'submitted', 'registration_date')
    search_fields = (
        'student__student_id', 
        'student__user__username', 
        'student__user__first_name', 
        'student__user__last_name'
    )
    ordering = ('-registration_date',)

@admin.register(RegistrationWindow)
class RegistrationWindowAdmin(admin.ModelAdmin):
    list_display = (
        'start_date', 
        'start_time', 
        'end_date', 
        'end_time', 
        'is_open'
    )
    list_filter = ('is_open', 'start_date', 'end_date')
    ordering = ('-start_date',)
