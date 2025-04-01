from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.utils import timezone
from accounts.models import StudentProfile, Department, Program, EnrollmentOfficerProfile
from .models import RegistrationWindow, StudentRegistration
from subjects.models import Subject
from studentSubjectCheckList.models import StudentSubjectChecklist
from datetime import time as time_

@login_required
@role_required(allowed_roles=['ADMIN'])
def open_registration_custom(request):
    window = RegistrationWindow.objects.last()
    
    if request.method == "POST":
        start_date_str = request.POST.get("start_date", "").strip()
        start_time_str = request.POST.get("start_time", "").strip()
        end_date_str = request.POST.get("end_date", "").strip()
        end_time_str = request.POST.get("end_time", "").strip()
        
        if not start_date_str or not start_time_str or not end_date_str or not end_time_str:
            messages.warning(request, "All date and time fields are required.")
            return render(request, "studentRegistration/open_registration_custom.html", {"window": window})
        
        try:
            start_date = timezone.datetime.strptime(start_date_str, "%b. %d, %Y").date()
            end_date = timezone.datetime.strptime(end_date_str, "%b. %d, %Y").date()
            start_time = timezone.datetime.strptime(start_time_str, "%I:%M%p").time()
            end_time = timezone.datetime.strptime(end_time_str, "%I:%M%p").time()
        except ValueError:
            messages.warning(request, "Invalid format. Use: Date: M. d, Y and Time: h:iA")
            return render(request, "studentRegistration/open_registration_custom.html", {"window": window})
        
        start_datetime = timezone.make_aware(timezone.datetime.combine(start_date, start_time), timezone.get_current_timezone())
        end_datetime = timezone.make_aware(timezone.datetime.combine(end_date, end_time), timezone.get_current_timezone())
        
        if end_datetime < start_datetime:
            messages.warning(request, "End date and time must be after the start date and time.")
            return render(request, "studentRegistration/open_registration_custom.html", {"window": window})
        
        if window:
            window.start_date = start_date
            window.start_time = start_time
            window.end_date = end_date
            window.end_time = end_time
            window.is_open = True
            window.save()
        else:
            RegistrationWindow.objects.create(
                start_date=start_date,
                start_time=start_time,
                end_date=end_date,
                end_time=end_time,
                is_open=True
            )
        messages.success(request, "Registration window set successfully and is now open.")
        return redirect('registration_calendar')
    
    context = {}
    if window:
        context["initial_start_date"] = window.start_date.strftime("%b. %d, %Y")
        context["initial_start_time"] = window.start_time.strftime("%I:%M%p")
        context["initial_end_date"] = window.end_date.strftime("%b. %d, %Y")
        context["initial_end_time"] = window.end_time.strftime("%I:%M%p")
        context["window"] = window
    return render(request, "studentRegistration/open_registration_custom.html", context)

@login_required
@role_required(allowed_roles=['ADMIN', 'OFFICER'])
def registration_calendar(request):
    window = RegistrationWindow.objects.last()
    return render(request, "studentRegistration/registration_calendar.html", {"window": window})



SECTIONS = [
    {'id': 'Section A', 'name': 'Section A'},
    {'id': 'Section B', 'name': 'Section B'},
    {'id': 'Section C', 'name': 'Section C'},
    {'id': 'Section D', 'name': 'Section D'},
    {'id': 'Section E', 'name': 'Section E'},
]
earliest_start = time_(7, 30)  
latest_end = time_(22, 0)
CLASS_DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
@login_required
def student_registration_form(request):
    if request.user.role.upper() != "STUDENT":
        messages.warning(request, "You are not allowed to access the registration form.")
        return redirect('home')
    
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    registration = StudentRegistration.objects.filter(student=student_profile).order_by('-registration_date').first()
    
    if registration and registration.submitted:
        return redirect('student_registration_detail_for_student', student_profile.student_id)
    
    available_minor_subjects = Subject.objects.filter(
        approved=True,
        subject_type='MINOR',
        programs=student_profile.program
    ).exclude(
        student_checklists__student=student_profile,
        student_checklists__taken=True
    ).distinct()
    
    form_data = {
        "preferred_section": "",
        "preferred_time_start_str": "",
        "preferred_time_end_str": "",
        "preferred_class_days_list": [],
        "additional_comments": "",
        "minor_priority_1": "",
        "minor_priority_2": "",
        "minor_priority_3": "",
        "minor_priority_4": "",
    }

    if request.method == "POST":
        form_data = {
            "preferred_section": request.POST.get("preferred_section", "").strip(),
            "additional_comments": request.POST.get("additional_comments", "").strip(),
            "preferred_time_start_str": request.POST.get("preferred_time_start", "").strip(),
            "preferred_time_end_str": request.POST.get("preferred_time_end", "").strip(),
            "preferred_class_days_list": request.POST.getlist("preferred_class_days"),
            "minor_priority_1": request.POST.get("minor_priority_1", "").strip(),
            "minor_priority_2": request.POST.get("minor_priority_2", "").strip(),
            "minor_priority_3": request.POST.get("minor_priority_3", "").strip(),
            "minor_priority_4": request.POST.get("minor_priority_4", "").strip(),
        }
        minor_choices = [choice for choice in [
            form_data["minor_priority_1"],
            form_data["minor_priority_2"],
            form_data["minor_priority_3"],
            form_data["minor_priority_4"]
        ] if choice]

        if not all([form_data["preferred_section"], form_data["preferred_time_start_str"], form_data["preferred_time_end_str"]]):
            messages.warning(request, "Please fill in all required fields.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        try:
            preferred_time_start = timezone.datetime.strptime(form_data["preferred_time_start_str"], "%I:%M%p").time()
            preferred_time_end = timezone.datetime.strptime(form_data["preferred_time_end_str"], "%I:%M%p").time()
        except ValueError:
            messages.warning(request, "Invalid time format. Please use: h:iA (e.g., 08:00AM).")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        if preferred_time_start < earliest_start:
            messages.error(request, "Start time cannot be earlier than 7:30 AM.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        if preferred_time_end > latest_end:
            messages.error(request, "End time cannot be later than 10:00 PM.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        if preferred_time_start >= preferred_time_end:
            messages.error(request, "End time must be greater than start time.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        if len(minor_choices) != len(set(minor_choices)):
            messages.warning(request, "Duplicate subjects in minor priorities.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        available_minor_ids = [str(sub.id) for sub in available_minor_subjects]
        for subject_id in minor_choices:
            if StudentSubjectChecklist.objects.filter(student=student_profile, subject_id=subject_id, taken=True).exists():
                messages.warning(request, f"You have already taken subject {subject_id}. Please choose a different subject.")
                return render(request, "studentRegistration/student_registration_form.html", {
                    "student_profile": student_profile,
                    "sections": SECTIONS,
                    "class_days": CLASS_DAYS,
                    "available_minor_subjects": available_minor_subjects,
                    "read_only": False,
                    "form_data": form_data,
                    "registration": registration,
                })
            if subject_id not in available_minor_ids:
                messages.warning(request, f"Subject {subject_id} is no longer available.")
                return render(request, "studentRegistration/student_registration_form.html", {
                    "student_profile": student_profile,
                    "sections": SECTIONS,
                    "class_days": CLASS_DAYS,
                    "available_minor_subjects": available_minor_subjects,
                    "read_only": False,
                    "form_data": form_data,
                    "registration": registration,
                })

        StudentRegistration.objects.create(
            student=student_profile,
            preferred_section=form_data["preferred_section"],
            preferred_time_start=preferred_time_start,
            preferred_time_end=preferred_time_end,
            preferred_class_days=",".join(form_data["preferred_class_days_list"]),
            selected_minor_subjects=",".join(minor_choices),
            additional_comments=form_data["additional_comments"],
            registration_date=timezone.now(),
            completed=False,
            submitted=True,
        )
        messages.success(request, "Registration submitted successfully!")
        return redirect('student_registration_detail_for_student', student_profile.student_id)

    context = {
        "student_profile": student_profile,
        "sections": SECTIONS,
        "class_days": CLASS_DAYS,
        "available_minor_subjects": available_minor_subjects,
        "read_only": False,
        "registration": registration,
        "form_data": form_data,
    }
    return render(request, "studentRegistration/student_registration_form.html", context)

@login_required
def student_registration_detail_for_student(request, student_id):
    if request.user.role.upper() != "STUDENT":
        messages.warning(request, "You are not allowed to access the registration detail.")
        return redirect('home')
    
    student_profile = get_object_or_404(StudentProfile, student_id=student_id)
    registration = StudentRegistration.objects.filter(student=student_profile).order_by('-registration_date').first()
    
    if not registration:
        messages.info(request, "You haven't submitted a registration form yet.")
        return redirect('student_registration_form')
    
    selected_minor_ids = registration.selected_minor_subjects.split(',') if registration.selected_minor_subjects else []
    selected_minor_subjects = Subject.objects.filter(id__in=selected_minor_ids)
    
    available_minor_subjects = Subject.objects.filter(
        approved=True,
        subject_type='MINOR',
        programs=student_profile.program
    ).exclude(
        student_checklists__student=student_profile,
        student_checklists__taken=True
    ).distinct()
    
    combined_minor_subjects = available_minor_subjects.union(selected_minor_subjects)
    
    form_data = {
        "minor_priority_1": selected_minor_ids[0] if len(selected_minor_ids) >= 1 else "",
        "minor_priority_2": selected_minor_ids[1] if len(selected_minor_ids) >= 2 else "",
        "minor_priority_3": selected_minor_ids[2] if len(selected_minor_ids) >= 3 else "",
        "minor_priority_4": selected_minor_ids[3] if len(selected_minor_ids) >= 4 else "",
        "preferred_section": registration.preferred_section,
        "preferred_time_start_str": registration.preferred_time_start.strftime("%I:%M%p"),
        "preferred_time_end_str": registration.preferred_time_end.strftime("%I:%M%p"),
        "preferred_class_days_list": registration.preferred_class_days.split(',') if registration.preferred_class_days else [],
        "additional_comments": registration.additional_comments,
    }
    
    context = {
        "student_profile": student_profile,
        "registration": registration,
        "sections": SECTIONS,
        "class_days": CLASS_DAYS,
        "available_minor_subjects": combined_minor_subjects,
        "read_only": True,
        "form_data": form_data,
    }
    return render(request, "studentRegistration/student_registration_form.html", context)

@login_required
def student_registration_edit(request):
    if request.user.role.upper() != "STUDENT":
        messages.warning(request, "You are not allowed to access the registration form.")
        return redirect('home')
    
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    registration = StudentRegistration.objects.filter(student=student_profile).order_by('-registration_date').first()
    
    if not registration:
        messages.warning(request, "No registration found to edit. Please submit one first.")
        return redirect('student_registration_form')

    available_minor_subjects = Subject.objects.filter(
        approved=True,
        subject_type='MINOR',
        programs=student_profile.program
    ).exclude(
        student_checklists__student=student_profile,
        student_checklists__taken=True
    ).distinct()

    existing_minor_choices = registration.selected_minor_subjects.split(',') if registration.selected_minor_subjects else []
    form_data = {
        "preferred_section": registration.preferred_section,
        "preferred_time_start_str": registration.preferred_time_start.strftime("%I:%M%p"),
        "preferred_time_end_str": registration.preferred_time_end.strftime("%I:%M%p"),
        "preferred_class_days_list": registration.preferred_class_days.split(',') if registration.preferred_class_days else [],
        "additional_comments": registration.additional_comments,
        "minor_priority_1": existing_minor_choices[0] if len(existing_minor_choices) >= 1 else "",
        "minor_priority_2": existing_minor_choices[1] if len(existing_minor_choices) >= 2 else "",
        "minor_priority_3": existing_minor_choices[2] if len(existing_minor_choices) >= 3 else "",
        "minor_priority_4": existing_minor_choices[3] if len(existing_minor_choices) >= 4 else "",
    }

    if request.method == "POST":
        form_data = {
            "preferred_section": request.POST.get("preferred_section", "").strip(),
            "preferred_time_start_str": request.POST.get("preferred_time_start", "").strip(),
            "preferred_time_end_str": request.POST.get("preferred_time_end", "").strip(),
            "preferred_class_days_list": request.POST.getlist("preferred_class_days"),
            "additional_comments": request.POST.get("additional_comments", "").strip(),
            "minor_priority_1": request.POST.get("minor_priority_1", "").strip(),
            "minor_priority_2": request.POST.get("minor_priority_2", "").strip(),
            "minor_priority_3": request.POST.get("minor_priority_3", "").strip(),
            "minor_priority_4": request.POST.get("minor_priority_4", "").strip(),
        }
        minor_choices = [choice for choice in [
            form_data["minor_priority_1"],
            form_data["minor_priority_2"],
            form_data["minor_priority_3"],
            form_data["minor_priority_4"]
        ] if choice]

        if not all([form_data["preferred_section"], form_data["preferred_time_start_str"], form_data["preferred_time_end_str"]]):
            messages.warning(request, "Please fill in all required fields.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "form_data": form_data,
                "read_only": False,
                "registration": registration,
            })

        try:
            preferred_time_start = timezone.datetime.strptime(form_data["preferred_time_start_str"], "%I:%M%p").time()
            preferred_time_end = timezone.datetime.strptime(form_data["preferred_time_end_str"], "%I:%M%p").time()
        except ValueError:
            messages.warning(request, "Invalid time format. Please use h:iA (e.g., 08:00AM).")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "form_data": form_data,
                "read_only": False,
                "registration": registration,
            })

        if preferred_time_start < earliest_start:
            messages.error(request, "Start time cannot be earlier than 7:30 AM.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        if preferred_time_end > latest_end:
            messages.error(request, "End time cannot be later than 10:00 PM.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        if preferred_time_start >= preferred_time_end:
            messages.error(request, "End time must be greater than start time.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "read_only": False,
                "form_data": form_data,
                "registration": registration,
            })

        if len(minor_choices) != len(set(minor_choices)):
            messages.warning(request, "Duplicate subjects in minor priorities.")
            return render(request, "studentRegistration/student_registration_form.html", {
                "student_profile": student_profile,
                "sections": SECTIONS,
                "class_days": CLASS_DAYS,
                "available_minor_subjects": available_minor_subjects,
                "form_data": form_data,
                "read_only": False,
                "registration": registration,
            })

        available_minor_ids = [str(sub.id) for sub in available_minor_subjects]
        for subject_id in minor_choices:
            if subject_id not in available_minor_ids and subject_id not in existing_minor_choices:
                messages.warning(request, f"Subject {subject_id} is no longer available.")
                return render(request, "studentRegistration/student_registration_form.html", {
                    "student_profile": student_profile,
                    "sections": SECTIONS,
                    "class_days": CLASS_DAYS,
                    "available_minor_subjects": available_minor_subjects,
                    "form_data": form_data,
                    "read_only": False,
                    "registration": registration,
                })
            if StudentSubjectChecklist.objects.filter(student=student_profile, subject_id=subject_id, taken=True).exists():
                messages.warning(request, f"You have already taken subject {subject_id}. Please choose a different subject.")
                return render(request, "studentRegistration/student_registration_form.html", {
                    "student_profile": student_profile,
                    "sections": SECTIONS,
                    "class_days": CLASS_DAYS,
                    "available_minor_subjects": available_minor_subjects,
                    "form_data": form_data,
                    "read_only": False,
                    "registration": registration,
                })

        registration.preferred_section = form_data["preferred_section"]
        registration.preferred_time_start = preferred_time_start
        registration.preferred_time_end = preferred_time_end
        registration.preferred_class_days = ",".join(form_data["preferred_class_days_list"])
        registration.selected_minor_subjects = ",".join(minor_choices)
        registration.additional_comments = form_data["additional_comments"]
        registration.completed = False
        registration.registration_date = timezone.now()
        registration.save()

        messages.success(request, "Registration updated successfully!")
        return redirect('student_registration_detail_for_student', student_profile.student_id)

    context = {
        "student_profile": student_profile,
        "sections": SECTIONS,
        "class_days": CLASS_DAYS,
        "available_minor_subjects": available_minor_subjects,
        "read_only": False,
        "form_data": form_data,
        "registration": registration,
    }
    return render(request, "studentRegistration/student_registration_form.html", context)




@login_required
@role_required(allowed_roles=['ADMIN', 'OFFICER'])
def student_registration_queue(request):
    base_regs = StudentRegistration.objects.select_related(
        'student__user',
        'student__department',
        'student__program'
    ).order_by('-registration_date')

    department_filter = request.GET.get('department')
    program_filter = request.GET.get('program')
    departments = None
    programs = None
    selected_department = None
    selected_program = None

    if request.user.role.upper() == "ADMIN" or request.user.is_superuser:
        departments = Department.objects.all()
        programs = Program.objects.all()
        selected_department = department_filter
        selected_program = program_filter
        
        if department_filter:
            base_regs = base_regs.filter(student__department__id=department_filter)
        if program_filter:
            base_regs = base_regs.filter(student__program__id=program_filter)
    else:
        try:
            officer_profile = EnrollmentOfficerProfile.objects.select_related('department').get(user=request.user)
            base_regs = base_regs.filter(student__department=officer_profile.department)
            programs = officer_profile.department.programs.all()
            selected_program = program_filter
            
            if program_filter:
                base_regs = base_regs.filter(student__program__id=program_filter)
        except EnrollmentOfficerProfile.DoesNotExist:
            messages.error(request, "Officer profile not found")
            return redirect('home')

    pending_regs = base_regs.filter(completed=False)
    completed_regs = base_regs.filter(completed=True)

    context = {
        'pending_regs': pending_regs,
        'completed_regs': completed_regs,
        'departments': departments,
        'programs': programs,
        'selected_department': selected_department,
        'selected_program': selected_program,
    }
    return render(request, "studentRegistration/student_registration_queue.html", context)


@login_required
@role_required(allowed_roles=['ADMIN', 'OFFICER'])
def student_registration_detail(request, student_id):
    student_profile = get_object_or_404(StudentProfile, student_id=student_id)
    registration = StudentRegistration.objects.filter(student=student_profile).order_by('-registration_date').first()
    
    minor_choices = []
    if registration and registration.selected_minor_subjects:
        minor_subject_ids = registration.selected_minor_subjects.split(',')
        minor_choices = Subject.objects.filter(id__in=minor_subject_ids).order_by('code')
    
    class_days = registration.preferred_class_days.split(',') if registration and registration.preferred_class_days else []
    
    all_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
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
    
    def get_checklist(subject_queryset):
        checklist = []
        for subject in subject_queryset:
            item, created = StudentSubjectChecklist.objects.get_or_create(
                student=student_profile,
                subject=subject
            )
            checklist.append(item)
        return checklist

    first_year_checklist = get_checklist(first_year_subjects)
    second_year_checklist = get_checklist(second_year_subjects)
    third_year_checklist = get_checklist(third_year_subjects)
    fourth_year_checklist = get_checklist(fourth_year_subjects)
    minor_checklist = get_checklist(minor_subjects)
    
    if request.method == "POST":
        subj_id = request.POST.get("subject_id")
        taken_value = request.POST.get("taken")
        taken = True if taken_value == "true" else False
        
        checklist_item = get_object_or_404(
            StudentSubjectChecklist,
            student=student_profile,
            subject_id=subj_id
        )
        checklist_item.taken = taken
        checklist_item.save()
        messages.success(request, "Subject status updated.")
        return redirect('student_registration_detail', student_id=student_id)
    
    context = {
        'student_profile': student_profile,
        'registration': registration,
        'class_days': class_days,  
        'all_days': all_days,      
        'minor_choices': minor_choices,
        'first_year_checklist': first_year_checklist,
        'second_year_checklist': second_year_checklist,
        'third_year_checklist': third_year_checklist,
        'fourth_year_checklist': fourth_year_checklist,
        'minor_checklist': minor_checklist,
    }
    return render(request, "studentRegistration/student_registration_detail.html", context)


@login_required
@role_required(allowed_roles=['ADMIN', 'OFFICER'])
def finalize_registration(request, student_id):
    student_profile = get_object_or_404(StudentProfile, student_id=student_id)
    
    registration = StudentRegistration.objects.filter(student=student_profile).order_by('-registration_date').first()
    
    if not registration:
        messages.warning(request, "No registration record found for this student.")
        return redirect('student_registration_queue')
    
    if request.method == "POST":
        uploaded_file = request.FILES.get("registration_form_image")
        print("Uploaded file:", uploaded_file)
        
        if not uploaded_file:
            messages.warning(request, "Please upload an image file.")
            return render(request, "studentRegistration/finalize_registration.html", {"registration": registration, "student_profile": student_profile})
        
        valid_types = ['image/jpeg', 'image/png', 'image/gif']
        if uploaded_file.content_type not in valid_types:
            messages.warning(request, "Only image files (JPEG, PNG, GIF) are allowed.")
            return render(request, "studentRegistration/finalize_registration.html", {"registration": registration, "student_profile": student_profile})
        
        registration.registration_form_image = uploaded_file
        registration.completed = True
        registration.save()
        messages.success(request, "Registration finalized successfully!")
        return redirect('student_registration_queue')
    
    context = {
        "registration": registration,
        "student_profile": student_profile,
    }
    return render(request, "studentRegistration/finalize_registration.html", context)


