from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'subject_type', 'year_level', 'get_departments',
        'semester', 'lec_units', 'lab_units', 'units', 'approved', 'created_at'
    )
    search_fields = ('code', 'name', 'description')
    list_filter = ('subject_type', 'year_level', 'departments', 'semester', 'approved')
    filter_horizontal = ('programs', 'prerequisites', 'departments',)

    def get_departments(self, obj):
        return ", ".join([dept.name for dept in obj.departments.all()])
    get_departments.short_description = "Departments"
