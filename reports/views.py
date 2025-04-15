from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import StudentProfile, Department, Program
from studentRegistration.models import StudentRegistration

# 1. Student List Report (all students, based on filter)
@login_required
def student_list_report(request):
    user_role = request.user.role.upper()
    selected_department = request.GET.get('department', '')
    selected_program = request.GET.get('program', '')

    if user_role == 'ADMIN' or request.user.is_superuser:
        students = StudentProfile.objects.all()
        if selected_department:
            students = students.filter(department__id=selected_department)
        if selected_program:
            students = students.filter(program__id=selected_program)
        departments = Department.objects.all()
        programs = Program.objects.filter(department__id=selected_department) if selected_department else Program.objects.all()
    elif user_role == 'OFFICER':
        dept = request.user.enrollmentofficerprofile.department
        students = StudentProfile.objects.filter(department=dept)
        if selected_program:
            students = students.filter(program__id=selected_program)
        departments = None
        programs = Program.objects.filter(department=dept)
    else:
        students = StudentProfile.objects.none()
        departments = None
        programs = None

    context = {
        'students': students,
        'departments': departments,
        'programs': programs,
        'selected_department': selected_department,
        'selected_program': selected_program,
        'user_role': user_role,
    }
    return render(request, 'reports/student_list_report.html', context)


# 2. Unregistered Student List Report
# List those students who don't have a submitted registration record.
@login_required
def unregistered_student_list_report(request):
    user_role = request.user.role.upper()
    selected_department = request.GET.get('department', '')
    selected_program = request.GET.get('program', '')

    if user_role == 'ADMIN' or request.user.is_superuser:
        students = StudentProfile.objects.all()
        if selected_department:
            students = students.filter(department__id=selected_department)
        if selected_program:
            students = students.filter(program__id=selected_program)
        departments = Department.objects.all()
        programs = Program.objects.filter(department__id=selected_department) if selected_department else Program.objects.all()
    elif user_role == 'OFFICER':
        dept = request.user.enrollmentofficerprofile.department
        students = StudentProfile.objects.filter(department=dept)
        if selected_program:
            students = students.filter(program__id=selected_program)
        departments = None
        programs = Program.objects.filter(department=dept)
    else:
        students = StudentProfile.objects.none()
        departments = None
        programs = None

    # Unregistered students: those with no registration record or latest record not submitted.
    unregistered_students = []
    for student in students:
        reg = student.registrations.order_by('-registration_date').first()
        if not reg or not reg.submitted:
            unregistered_students.append(student)
    
    context = {
        'students': unregistered_students,
        'departments': departments,
        'programs': programs,
        'selected_department': selected_department,
        'selected_program': selected_program,
        'user_role': user_role,
    }
    return render(request, 'reports/unregistered_student_list_report.html', context)


# 3. Registered/Pending Registration Student Report
# Students with a registration record that is submitted but not completed.
@login_required
def pending_registration_student_report(request):
    user_role = request.user.role.upper()
    selected_department = request.GET.get('department', '')
    selected_program = request.GET.get('program', '')

    if user_role == 'ADMIN' or request.user.is_superuser:
        students = StudentProfile.objects.all()
        if selected_department:
            students = students.filter(department__id=selected_department)
        if selected_program:
            students = students.filter(program__id=selected_program)
        departments = Department.objects.all()
        programs = Program.objects.filter(department__id=selected_department) if selected_department else Program.objects.all()
    elif user_role == 'OFFICER':
        dept = request.user.enrollmentofficerprofile.department
        students = StudentProfile.objects.filter(department=dept)
        if selected_program:
            students = students.filter(program__id=selected_program)
        departments = None
        programs = Program.objects.filter(department=dept)
    else:
        students = StudentProfile.objects.none()
        departments = None
        programs = None

    pending_students = []
    for student in students:
        reg = student.registrations.order_by('-registration_date').first()
        if reg and reg.submitted and not reg.completed:
            pending_students.append(student)
    
    context = {
        'students': pending_students,
        'departments': departments,
        'programs': programs,
        'selected_department': selected_department,
        'selected_program': selected_program,
        'user_role': user_role,
    }
    return render(request, 'reports/pending_registration_student_report.html', context)


# 4. Completed Registration Student List Report
@login_required
def completed_registration_student_list_report(request):
    user_role = request.user.role.upper()
    selected_department = request.GET.get('department', '')
    selected_program = request.GET.get('program', '')
    
    if user_role == 'ADMIN' or request.user.is_superuser:
        students = StudentProfile.objects.all()
        if selected_department:
            students = students.filter(department__id=selected_department)
        if selected_program:
            students = students.filter(program__id=selected_program)
        departments = Department.objects.all()
        programs = Program.objects.filter(department__id=selected_department) if selected_department else Program.objects.all()
    elif user_role == 'OFFICER':
        dept = request.user.enrollmentofficerprofile.department
        students = StudentProfile.objects.filter(department=dept)
        if selected_program:
            students = students.filter(program__id=selected_program)
        departments = None
        programs = Program.objects.filter(department=dept)
    else:
        students = StudentProfile.objects.none()
        departments = None
        programs = None

    completed_students = []
    for student in students:
        reg = student.registrations.order_by('-registration_date').first()
        if reg and reg.completed:
            completed_students.append(student)
    
    context = {
        'students': completed_students,
        'departments': departments,
        'programs': programs,
        'selected_department': selected_department,
        'selected_program': selected_program,
        'user_role': user_role,
    }
    return render(request, 'reports/completed_registration_student_list_report.html', context)
