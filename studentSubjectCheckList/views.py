from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from subjects.models import Subject
from .models import StudentSubjectChecklist
from accounts.models import StudentProfile

@login_required
def subject_checklist(request):
    student = request.user
    student_profile = get_object_or_404(StudentProfile, user=student)
    
    major_subjects = Subject.objects.filter(
        approved=True,
        subject_type='MAJOR',
        departments=student_profile.department,
        programs=student_profile.program
    ).distinct()
    
    first_year_subjects = major_subjects.filter(year_level=1)
    second_year_subjects = major_subjects.filter(year_level=2)
    third_year_subjects = major_subjects.filter(year_level=3)
    fourth_year_subjects = major_subjects.filter(year_level=4)

    minor_subjects = Subject.objects.filter(
        approved=True,
        subject_type='MINOR',
        programs=student_profile.program
    ).distinct()
    
    def get_checklist_for_subjects(subject_queryset):
        checklist = []
        for subject in subject_queryset:
            item, created = StudentSubjectChecklist.objects.get_or_create(
                student=student,
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
            student=student,
            subject_id=subject_id
        )
        checklist_item.taken = taken
        checklist_item.save()
        return redirect('subject_checklist')  
    
    context = {
        'first_year_checklist': first_year_checklist,
        'second_year_checklist': second_year_checklist,
        'third_year_checklist': third_year_checklist,
        'fourth_year_checklist': fourth_year_checklist,
        'minor_checklist': minor_checklist,
        'student_profile': student_profile,
    }
    return render(request, "studentSubjectChecklist/subject_checklist.html", context)
