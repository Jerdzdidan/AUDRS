from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from accounts.models import Department, Program, EnrollmentOfficerProfile
from .models import Subject

@login_required
@role_required(allowed_roles=['OFFICER', 'ADMIN'])
def subject_list_department(request):
    if request.user.role == 'ADMIN':
        departments = Department.objects.all()
        department_id = request.GET.get('department')
        if department_id:
            department = get_object_or_404(Department, id=department_id)
            programs = department.programs.all()
        else:
            department = None
            programs = Program.objects.all()
        base_queryset = Subject.objects.filter(approved=True)
        if department:
            base_queryset = base_queryset.filter(department=department)
    else:
        departments = None
        officer_profile = get_object_or_404(EnrollmentOfficerProfile, user=request.user)
        department = officer_profile.department
        programs = department.programs.all()
        base_queryset = Subject.objects.filter(department=department, approved=True)
    
    program_id = request.GET.get('program')
    if program_id:
        base_queryset = base_queryset.filter(programs=program_id)
    
    first_year_subjects  = base_queryset.filter(subject_type='MAJOR', year_level=1)
    second_year_subjects = base_queryset.filter(subject_type='MAJOR', year_level=2)
    third_year_subjects  = base_queryset.filter(subject_type='MAJOR', year_level=3)
    fourth_year_subjects = base_queryset.filter(subject_type='MAJOR', year_level=4)
    minor_subjects       = base_queryset.filter(subject_type='MINOR')
    
    context = {
        'selected_program': program_id,
        'first_year_subjects': first_year_subjects,
        'second_year_subjects': second_year_subjects,
        'third_year_subjects': third_year_subjects,
        'fourth_year_subjects': fourth_year_subjects,
        'minor_subjects': minor_subjects,
        'departments': departments,
        'selected_department': department,
        'programs': programs,
    }
    return render(request, 'subjects/subject_list_department.html', context)
