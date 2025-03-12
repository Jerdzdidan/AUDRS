from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, StudentProfile, EnrollmentOfficerProfile, Program

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    search_fields = ('username', 'email', 'role')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'program', 'year_level', 'department')
    search_fields = ('user__username', 'student_id', 'program')
    list_filter = ('department',)

@admin.register(EnrollmentOfficerProfile)
class EnrollmentOfficerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'office_number')
    search_fields = ('user__username', 'office_number')
    list_filter = ('department',)
