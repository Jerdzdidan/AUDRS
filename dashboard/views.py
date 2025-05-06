from django.shortcuts import render
from studentRegistration.models import StudentRegistration
from accounts.models import StudentProfile, Department, Program
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user_role = request.user.role.upper()
    
    # Get filter parameters from the query string.
    selected_department = request.GET.get('department', '')
    selected_program = request.GET.get('program', '')
    
    if user_role == 'ADMIN' or request.user.is_superuser:
        students_qs = StudentProfile.objects.all()
        registrations_qs = StudentRegistration.objects.all()
        if selected_department:
            students_qs = students_qs.filter(department__id=selected_department)
            registrations_qs = registrations_qs.filter(student__department__id=selected_department)
            programs = Program.objects.filter(department__id=selected_department)
        else:
            programs = Program.objects.all()

        if selected_program:
            students_qs = students_qs.filter(program__id=selected_program)
            registrations_qs = registrations_qs.filter(student__program__id=selected_program)

        departments = Department.objects.all()
        
    elif user_role == 'OFFICER':
        dept = request.user.enrollmentofficerprofile.department
        students_qs = StudentProfile.objects.filter(department=dept)
        registrations_qs = StudentRegistration.objects.filter(student__department=dept)
        if selected_program:
            students_qs = students_qs.filter(program__id=selected_program)
            registrations_qs = registrations_qs.filter(student__program__id=selected_program)
        departments = None  # Not needed for officers.
        programs = Program.objects.filter(department=dept)
    else:
        students_qs = StudentProfile.objects.none()
        registrations_qs = StudentRegistration.objects.none()
        departments = None
        programs = None
    
    # Calculate metrics.
    total_students = students_qs.count()
    total_registrations = registrations_qs.count()
    completed_count = registrations_qs.filter(completed=True).count()
    pending_count = registrations_qs.filter(completed=False).count()
    
    # For officer users: fetch 5 most recent pending registrations.
    pending_registrations = None
    if user_role == 'OFFICER':
        pending_registrations = registrations_qs.filter(completed=False).order_by('-registration_date')[:5]
    
    context = {
        'user_role': user_role,
        'total_students': total_students,
        'total_registrations': total_registrations,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'departments': departments,
        'programs': programs,
        'selected_department': selected_department,
        'selected_program': selected_program,
        'pending_registrations': pending_registrations,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
