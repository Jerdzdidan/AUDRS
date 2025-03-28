from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from accounts.models import Department, Program, EnrollmentOfficerProfile
from .models import Subject
from django.contrib import messages

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
            base_queryset = Subject.objects.filter(departments__id=department.id)
    else:
        departments = None
        officer_profile = get_object_or_404(EnrollmentOfficerProfile, user=request.user)
        department = officer_profile.department
        programs = department.programs.all()
        base_queryset = Subject.objects.filter(departments__id=department.id)
    
    program_id = request.GET.get('program')
    if program_id:
        base_queryset = base_queryset.filter(programs__id=program_id)
    
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

@login_required
@role_required(allowed_roles=['OFFICER', 'ADMIN'])
def create_subject(request):
    if request.method == 'POST':
        raw_code = request.POST.get('code', '')
        code = raw_code.strip().replace(" ", "")
        
        name = request.POST.get('name', '').strip()
        subject_type = request.POST.get('subject_type')
        year_level = request.POST.get('year_level') if subject_type == 'MAJOR' else None
        semester = request.POST.get('semester') if subject_type == 'MAJOR' else "--"
        lec_units = request.POST.get('lec_units') or '3'
        lab_units = request.POST.get('lab_units') or '0'
        units = request.POST.get('units') or '3'
        description = request.POST.get('description', '').strip()
        
        prereq_ids = request.POST.getlist('prerequisites')
        prog_ids = request.POST.getlist('programs')
        
        if request.user.role == 'OFFICER':
            officer_profile = get_object_or_404(EnrollmentOfficerProfile, user=request.user)
            dept_ids = [str(officer_profile.department.id)]
        else:
            dept_ids = request.POST.getlist('departments')
        
        if not (code and subject_type):
            messages.warning(request, "Subject Code and Subject Type are required.")
            return redirect('subject-management-create-subject')
        
        approved_status = True if request.user.role == 'ADMIN' else False

        existing_subject = Subject.objects.filter(code=code).first()
        if existing_subject:
            name = existing_subject.name
            subject_type = existing_subject.subject_type
            year_level = existing_subject.year_level
            semester = existing_subject.semester
            lec_units = existing_subject.lec_units
            lab_units = existing_subject.lab_units
            units = existing_subject.units
            description = existing_subject.description

            if dept_ids:
                existing_subject.departments.add(*dept_ids)
            if prog_ids:
                existing_subject.programs.add(*prog_ids)
            if prereq_ids:
                existing_subject.prerequisites.add(*prereq_ids)
            
            if request.user.role == 'ADMIN':
                existing_subject.approved = True
            
            existing_subject.save()
            messages.success(request, f"Subject {existing_subject.code} already exists. Details were auto-assigned and associations updated.")
        else:
            subject = Subject.objects.create(
                name=name,
                code=code,
                subject_type=subject_type,
                year_level=year_level,
                semester=semester,
                lec_units=lec_units,
                lab_units=lab_units,
                units=units,
                description=description,
                approved=approved_status
            )
            if dept_ids:
                subject.departments.set(dept_ids)
            if prog_ids:
                subject.programs.set(prog_ids)
            if prereq_ids:
                subject.prerequisites.set(prereq_ids)
            subject.save()
            if approved_status:
                messages.success(request, "Subject created successfully and is approved.")
            else:
                messages.success(request, "Subject registered successfully and is pending admin approval.")
        
        return redirect('subject-management-list')
    
    context = {}
    if request.user.role == 'ADMIN':
        context['departments'] = Department.objects.all()
        context['programs'] = Program.objects.all()
    else:
        officer_profile = get_object_or_404(EnrollmentOfficerProfile, user=request.user)
        context['fixed_department'] = officer_profile.department
        context['programs'] = officer_profile.department.programs.all()
    context['all_subjects'] = Subject.objects.all().order_by('code')
    return render(request, 'subjects/create_subject.html', context)



@login_required
@role_required(allowed_roles=['OFFICER', 'ADMIN'])
def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()
        subject_type = request.POST.get('subject_type')
        year_level = request.POST.get('year_level') if subject_type == 'MAJOR' else None
        semester = request.POST.get('semester') if subject_type == 'MAJOR' else "--"
        lec_units = request.POST.get('lec_units') or '3'
        lab_units = request.POST.get('lab_units') or '0'
        units = request.POST.get('units') or '3'
        description = request.POST.get('description', '').strip()
        
        prereq_ids = request.POST.getlist('prerequisites')
        prog_ids = request.POST.getlist('programs')
        
        if request.user.role == 'OFFICER':
            officer_profile = get_object_or_404(EnrollmentOfficerProfile, user=request.user)
            dept_ids = [str(officer_profile.department.id)]
        else:
            dept_ids = request.POST.getlist('departments')
        
        if not (name and code and subject_type):
            messages.warning(request, "Name, Code, and Subject Type are required.")
            return redirect('subject-management-update-subject', subject_id=subject_id)
        
        if request.user.role == 'ADMIN':
            subject.approved = True
        
        subject.name = name
        subject.code = code
        subject.subject_type = subject_type
        subject.year_level = year_level
        subject.semester = semester
        subject.lec_units = lec_units
        subject.lab_units = lab_units
        subject.units = units
        subject.description = description
        
        subject.save()
        
        if dept_ids:
            subject.departments.set(dept_ids)
        if prog_ids:
            subject.programs.set(prog_ids)
        if prereq_ids:
            subject.prerequisites.set(prereq_ids)
        
        subject.save()
        
        messages.success(request, f"Subject {subject.code} updated successfully.")
        return redirect('subject-management-list')
    
    context = {'subject': subject}
    if request.user.role == 'ADMIN':
        context['departments'] = Department.objects.all()
        context['programs'] = Program.objects.all()
    else:
        officer_profile = get_object_or_404(EnrollmentOfficerProfile, user=request.user)
        context['fixed_department'] = officer_profile.department
        context['programs'] = officer_profile.department.programs.all()
    
    context['all_subjects'] = Subject.objects.all().order_by('code')
    
    return render(request, 'subjects/update_subject.html', context)


@login_required
@role_required(allowed_roles=['ADMIN'])
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully.")
    return redirect('subject-management-list')


@login_required
@role_required(allowed_roles=['ADMIN'])
def subject_approval_queue(request):
    pending_subjects = Subject.objects.filter(approved=False)
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        action = request.POST.get('action')  
        subject = get_object_or_404(Subject, id=subject_id)
        if action == 'approve':
            subject.approved = True
            subject.save()
            messages.success(request, f"Subject {subject.code} approved.")
        elif action == 'reject':
            subject.delete()
            messages.success(request, f"Subject {subject.code} rejected and deleted.")
        return redirect('subject-management-list')
    
    context = {
        'pending_subjects': pending_subjects,
    }
    return render(request, 'subjects/subject_approval_queue.html', context)