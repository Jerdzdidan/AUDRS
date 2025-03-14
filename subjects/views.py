from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject
from accounts.models import Department, EnrollmentOfficerProfile

@login_required
def subject_management_list(request):
    # Only ADMIN, OFFICER, and SUPERUSER can manage subjects.
    if request.user.role not in ['ADMIN', 'OFFICER', 'SUPERUSER']:
        messages.warning(request, "Unauthorized access")
        return redirect('home')
    
    # Officers see only subjects in their department.
    if request.user.role.lower() == 'officer':
        try:
            officer_profile = EnrollmentOfficerProfile.objects.get(user=request.user)
            subjects = Subject.objects.filter(department=officer_profile.department)
        except EnrollmentOfficerProfile.DoesNotExist:
            messages.warning(request, "Your officer profile was not found")
            return redirect('home')
    else:
        subjects = Subject.objects.all()
    
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})

@login_required
def create_subject(request):
    if request.user.role not in ['ADMIN', 'OFFICER', 'SUPERUSER']:
        messages.warning(request, "Unauthorized access")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        subject_type = request.POST.get('subject_type')
        units = request.POST.get('units')
        description = request.POST.get('description')
        year_level = request.POST.get('year_level')  # Can be blank for minor subjects
        prerequisites_ids = request.POST.getlist('prerequisites')
        
        # Determine the department:
        if request.user.role.lower() == 'officer':
            try:
                officer_profile = EnrollmentOfficerProfile.objects.get(user=request.user)
                department = officer_profile.department
            except EnrollmentOfficerProfile.DoesNotExist:
                messages.warning(request, "Your officer profile was not found")
                return redirect('home')
        else:
            department = get_object_or_404(Department, id=request.POST.get('department'))
        
        subject = Subject.objects.create(
            name=name,
            code=code,
            subject_type=subject_type,
            units=units,
            description=description,
            year_level=year_level,
            department=department,
            approved=False  # For now, approval can be set later by admin
        )
        if prerequisites_ids:
            subject.prerequisites.set(prerequisites_ids)
        messages.success(request, "Subject created successfully")
        return redirect('subject-list')
    
    # Prepare context for GET.
    context = {}
    if request.user.role.lower() != 'officer':
        context['departments'] = Department.objects.all()
    context['subject_types'] = Subject.SUBJECT_TYPE_CHOICES
    context['year_levels'] = Subject.YEAR_LEVEL_CHOICES
    # For prerequisites, we list subjects within the selected department if available.
    # For officers, use their fixed department; for admin, list all or you may filter by a selected department.
    if request.user.role.lower() == 'officer':
        try:
            officer_profile = EnrollmentOfficerProfile.objects.get(user=request.user)
            context['prerequisites'] = Subject.objects.filter(department=officer_profile.department)
        except EnrollmentOfficerProfile.DoesNotExist:
            context['prerequisites'] = Subject.objects.none()
    else:
        context['prerequisites'] = Subject.objects.all()
    
    return render(request, 'subjects/create_subject.html', context)

@login_required
def update_subject(request, subject_id):
    if request.user.role not in ['ADMIN', 'OFFICER', 'SUPERUSER']:
        messages.warning(request, "Unauthorized access")
        return redirect('home')
    
    subject = get_object_or_404(Subject, id=subject_id)
    
    # For officers, ensure they only update subjects within their department.
    if request.user.role.lower() == 'officer':
        try:
            officer_profile = EnrollmentOfficerProfile.objects.get(user=request.user)
            if subject.department != officer_profile.department:
                messages.warning(request, "You cannot update a subject outside your department")
                return redirect('subject-list')
        except EnrollmentOfficerProfile.DoesNotExist:
            messages.warning(request, "Your officer profile was not found")
            return redirect('home')
    
    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.code = request.POST.get('code')
        subject.subject_type = request.POST.get('subject_type')
        subject.units = request.POST.get('units')
        subject.description = request.POST.get('description')
        subject.year_level = request.POST.get('year_level')
        # Only allow non-officers to update department.
        if request.user.role.lower() != 'officer':
            subject.department = get_object_or_404(Department, id=request.POST.get('department'))
        prerequisites_ids = request.POST.getlist('prerequisites')
        subject.save()
        if prerequisites_ids:
            subject.prerequisites.set(prerequisites_ids)
        else:
            subject.prerequisites.clear()
        messages.success(request, "Subject updated successfully")
        return redirect('subject-list')
    
    context = {'subject': subject}
    if request.user.role.lower() != 'officer':
        context['departments'] = Department.objects.all()
    context['subject_types'] = Subject.SUBJECT_TYPE_CHOICES
    context['year_levels'] = Subject.YEAR_LEVEL_CHOICES
    # List prerequisites (you may list subjects within the same department)
    context['prerequisites'] = Subject.objects.filter(department=subject.department)
    return render(request, 'subjects/update_subject.html', context)
