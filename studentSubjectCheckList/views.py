from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from subjects.models import Subject
from .models import StudentSubjectChecklist
from accounts.decorators import role_required
from accounts.models import StudentProfile, EnrollmentOfficerProfile, Department, Program
from django.contrib import messages

@login_required
def student_list_for_checklist(request):
    if request.user.role.upper() == "ADMIN" or request.user.is_superuser:
        student_profiles = StudentProfile.objects.all()
        department_filter = request.GET.get('department')
        program_filter = request.GET.get('program')
        
        if department_filter:
            student_profiles = student_profiles.filter(department__id=department_filter)
        if program_filter:
            student_profiles = student_profiles.filter(program__id=program_filter)
        
        departments = Department.objects.all()
        programs = Program.objects.all()
        selected_department = department_filter
        selected_program = program_filter
    else:
        officer_profile = get_object_or_404(EnrollmentOfficerProfile, user=request.user)
        student_profiles = StudentProfile.objects.filter(department=officer_profile.department)
        program_filter = request.GET.get('program')
        if program_filter:
            student_profiles = student_profiles.filter(program__id=program_filter)
        
        departments = None 
        programs = officer_profile.department.programs.all()
        selected_department = None
        selected_program = program_filter

    context = {
        'student_profiles': student_profiles,
        'departments': departments,
        'programs': programs,
        'selected_department': selected_department,
        'selected_program': selected_program,
    }
    return render(request, "studentSubjectChecklist/student_list_for_checklist.html", context)


@login_required
def subject_checklist(request, student_id):
    student_profile = get_object_or_404(StudentProfile, student_id=student_id)
    
    major_subjects = Subject.objects.filter(
        approved=True,
        subject_type='MAJOR',
        departments=student_profile.department,
        programs=student_profile.program
    ).distinct()
    
    first_year_subjects = major_subjects.filter(year_level=1).order_by('code')
    second_year_subjects = major_subjects.filter(year_level=2).order_by('code')
    third_year_subjects = major_subjects.filter(year_level=3).order_by('code')
    fourth_year_subjects = major_subjects.filter(year_level=4).order_by('code')

    minor_subjects = Subject.objects.filter(
        approved=True,
        subject_type='MINOR',
        programs=student_profile.program
    ).distinct()
    
    def get_checklist_for_subjects(subject_queryset):
        checklist = []
        for subject in subject_queryset:
            item, created = StudentSubjectChecklist.objects.get_or_create(
                student=student_profile,
                subject=subject
            )
            checklist.append(item)
        return checklist
    
    first_year_checklist  = get_checklist_for_subjects(first_year_subjects)
    second_year_checklist = get_checklist_for_subjects(second_year_subjects)
    third_year_checklist  = get_checklist_for_subjects(third_year_subjects)
    fourth_year_checklist = get_checklist_for_subjects(fourth_year_subjects)
    minor_checklist       = get_checklist_for_subjects(minor_subjects)
    
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        taken_value = request.POST.get("taken")  
        taken = True if taken_value == "true" else False
        
        checklist_item = get_object_or_404(
            StudentSubjectChecklist,
            student=student_profile,
            subject_id=subject_id
        )
        checklist_item.taken = taken
        checklist_item.save()
        return redirect('student-subject-checklist', student_id)
    
    context = {
        'first_year_checklist': first_year_checklist,
        'second_year_checklist': second_year_checklist,
        'third_year_checklist': third_year_checklist,
        'fourth_year_checklist': fourth_year_checklist,
        'minor_checklist': minor_checklist,
        'student_profile': student_profile,
    }
    return render(request, "studentSubjectChecklist/student_subject_checklist.html", context)

