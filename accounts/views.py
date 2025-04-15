from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, StudentProfile, EnrollmentOfficerProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department, Program
from .decorators import role_required
from django.core.exceptions import ObjectDoesNotExist
from systemLogs.models import Logs
from datetime import datetime

now = datetime.now()

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, "Invalid credentials")
        return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')

@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

# ---------------------------
# Account Management Views
# ---------------------------
@login_required
@role_required(allowed_roles=['ADMIN', 'OFFICER'])
def accounts_list_students(request):
    if request.user.role == 'ADMIN':
        students = CustomUser.objects.filter(
            role='STUDENT', 
            is_superuser=False
        ).exclude(id=request.user.id)
    elif request.user.role == 'OFFICER':
        try:
            officer_profile = EnrollmentOfficerProfile.objects.get(user=request.user)
            students = CustomUser.objects.filter(
                role='STUDENT',
                studentprofile__department=officer_profile.department,
                is_superuser=False
            ).exclude(id=request.user.id)
        except EnrollmentOfficerProfile.DoesNotExist:
            messages.error(request, "Your officer profile was not found")
            return redirect('home')
    else:
        students = CustomUser.objects.filter(
            role='STUDENT', 
            is_superuser=False
        ).exclude(id=request.user.id)
    
    return render(request, 'accounts/accounts_list_students.html', {'students': students})


@login_required
@role_required(allowed_roles=['ADMIN'])
def accounts_list_officers(request):
    officers = CustomUser.objects.filter(
        role='OFFICER',
        is_superuser=False
    )
    return render(request, 'accounts/accounts_list_officers.html', {'officers': officers})

@login_required
@role_required(allowed_roles=['SUPERUSER'])
def accounts_list_admins(request):
    admins = CustomUser.objects.filter(role='ADMIN')
    return render(request, 'accounts/accounts_list_admins.html', {'admins': admins})

@login_required
def create_user(request):
    creator = request.user
    if creator.role not in ['ADMIN', 'OFFICER', 'SUPERUSER']:
        messages.warning(request, "Unauthorized access")
        return redirect('home')
    
    context = {}
    if creator.role.lower() != 'officer':
        dept_id = request.GET.get('dept')
        if dept_id:
            selected_department = get_object_or_404(Department, id=dept_id)
        else:
            selected_department = Department.objects.first()  
        context['departments'] = Department.objects.all()
        context['selected_department'] = selected_department
        context['programs'] = Program.objects.filter(department=selected_department)
        context['roles'] = ['ADMIN', 'OFFICER', 'STUDENT']
    else:
        try:
            officer_profile = EnrollmentOfficerProfile.objects.get(user=creator)
            fixed_department = officer_profile.department
        except EnrollmentOfficerProfile.DoesNotExist:
            messages.warning(request, "Your officer profile was not found")
            return redirect('home')
        context['fixed_department'] = fixed_department
        context['programs'] = Program.objects.filter(department=fixed_department)
    
    if request.method == 'POST':
        if creator.role.lower() == 'officer':
            role = 'STUDENT'
        else:
            role = request.POST.get('role')
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists. Please choose a different one.")
            return render(request, 'accounts/create_user.html', context)
        
        if creator.role.lower() == 'officer':
            try:
                officer_profile = EnrollmentOfficerProfile.objects.get(user=creator)
                department = officer_profile.department
            except EnrollmentOfficerProfile.DoesNotExist:
                messages.warning(request, "Your officer profile was not found")
                return redirect('home')
        else:
            department = get_object_or_404(Department, id=request.POST.get('department'))
        
        if role == 'STUDENT':
            program = get_object_or_404(Program, id=request.POST.get('program'))
            year_level = request.POST.get('year_level')
        else:
            program = None
            year_level = None
        
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                role=role,
                first_name=first_name,
                last_name=last_name,
                created_by=creator
            )
            if role == 'STUDENT':
                if StudentProfile.objects.filter(student_id=request.POST.get('student_id')).exists():
                    messages.warning(request, "A student with that Student ID already exists. Please use a different Student ID.")
                    return redirect('create-user')
                StudentProfile.objects.create(
                    user=user,
                    student_id=request.POST.get('student_id'),
                    program=program,
                    year_level=year_level,
                    department=department
                )
            elif role == 'OFFICER':
                EnrollmentOfficerProfile.objects.create(
                    user=user,
                    department=department,
                    office_number=''  
                )
            messages.success(request, "User created successfully")

            if role == 'STUDENT':
                return redirect('student-list')
            elif role == 'OFFICER':
                return redirect('officer-list')
            elif role == 'ADMIN':
                return redirect('admin-list')
            else:
                return redirect('home')

        except Exception as e:
            messages.warning(request, str(e))
            return render(request, 'accounts/create_user.html', context)
    
    return render(request, 'accounts/create_user.html', context)


@login_required
def update_user(request, user_id):
    try:
        user_obj = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.warning(request, "User not found")
        return redirect('student-list')

    if request.user.role not in ['ADMIN', 'OFFICER'] and request.user.id != user_obj.id:
        messages.warning(request, "You don't have permission to edit this account")
        return redirect('home')

    if request.method == 'POST':
        user_obj.email = request.POST.get('email')
        if password := request.POST.get('password'):
            user_obj.set_password(password)
        
        user_obj.is_active = request.POST.get('is_active', 'true').lower() == 'true'
        
        if request.user.is_superuser:
            new_role = request.POST.get('role')
            if new_role != user_obj.role:
                if user_obj.role == 'STUDENT':
                    StudentProfile.objects.filter(user=user_obj).delete()
                elif user_obj.role == 'OFFICER':
                    EnrollmentOfficerProfile.objects.filter(user=user_obj).delete()
                
                user_obj.role = new_role
                if new_role == 'STUDENT':
                    StudentProfile.objects.create(user=user_obj)
                elif new_role == 'OFFICER':
                    EnrollmentOfficerProfile.objects.create(user=user_obj)

        user_obj.save()

        if user_obj.role == 'STUDENT':
            profile = StudentProfile.objects.get(user=user_obj)
            profile.student_id = request.POST.get('student_id', '')
            
            if department_id := request.POST.get('department'):
                profile.department = get_object_or_404(Department, id=department_id)
            
            if program_id := request.POST.get('program'):
                profile.program = get_object_or_404(Program, id=program_id)
            
            profile.year_level = request.POST.get('year_level', 1)
            profile.save()

        elif user_obj.role == 'OFFICER':
            profile = EnrollmentOfficerProfile.objects.get(user=user_obj)
            if department_id := request.POST.get('department'):
                profile.department = get_object_or_404(Department, id=department_id)
                profile.save()
        
        formatted_date = now.strftime("%b. %d, %Y")
        formatted_time = now.strftime("%I:%M%p")
        Logs.objects.create(
            datelog=datetime.strptime(formatted_date, "%b. %d, %Y").date(),
            timelog=datetime.strptime(formatted_time, "%I:%M%p").time(),
            module="Accounts Management",
            action="Update User",
            performed_to=f"user: {user_obj.username} - {user_obj.last_name}, {user_obj.first_name}",
            performed_by= f"username: {request.user.username} - {request.user.last_name}, {request.user.first_name}"
        )

        messages.success(request, "Account updated successfully")
        if user_obj == request.user:
            return redirect('home')
        else:
            if user_obj.role == 'STUDENT':
                return redirect('student-list')
            elif user_obj.role == 'OFFICER':
                return redirect('officer-list')
            elif user_obj.role == 'ADMIN':
                return redirect('admin-list')
            else:
                return redirect('home')

    context = {
        'user_obj': user_obj,
        'departments': Department.objects.all(),
        'roles': ['ADMIN', 'OFFICER', 'STUDENT'] if request.user.is_superuser else []
    }

    try:
        if user_obj.role == 'STUDENT':
            profile = StudentProfile.objects.get(user=user_obj)
            context['profile'] = profile
            context['programs'] = Program.objects.filter(department=profile.department)
        elif user_obj.role == 'OFFICER':
            context['profile'] = EnrollmentOfficerProfile.objects.get(user=user_obj)
    except ObjectDoesNotExist:
        messages.warning(request, "Profile not found")
        return redirect('home')

    return render(request, 'accounts/update_user.html', context)

@login_required
@role_required(allowed_roles=['ADMIN'])
def delete_user(request, user_id):
    if request.user.role not in ['ADMIN', 'OFFICER', 'SUPERUSER']:
        messages.warning(request, "Unauthorized access")
        return redirect('home')
    
    try:
        user_obj = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.warning(request, "User not found")
        return redirect(request.META.get('HTTP_REFERER', 'student-list'))
    
    formatted_date = now.strftime("%b. %d, %Y")
    formatted_time = now.strftime("%I:%M%p")
    Logs.objects.create(
        datelog=datetime.strptime(formatted_date, "%b. %d, %Y").date(),
        timelog=datetime.strptime(formatted_time, "%I:%M%p").time(),
        module="Accounts Management",
        action="Delete User",
        performed_to=f"user: {user_obj.username} - {user_obj.last_name}, {user_obj.first_name}",
        performed_by= f"username: {request.user.username} - {request.user.last_name}, {request.user.first_name}"
    )
    
    user_obj.delete()
    messages.success(request, "User deleted successfully")
    return redirect(request.META.get('HTTP_REFERER', 'student-list'))
