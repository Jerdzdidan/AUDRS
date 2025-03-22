from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLES = (
        ('SUPERUSER', 'Superuser'),
        ('ADMIN', 'Admin'),
        ('OFFICER', 'Enrollment Officer'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='ADMIN')
    email = models.EmailField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users"
    )

    def save(self, *args, **kwargs):
        self.role = self.role.upper()  
        if self.role == 'ADMIN':
            self.is_superuser = True
            self.is_staff = True
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Program(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('department', 'name')
        ordering = ['name']
    
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE) 
    year_level = models.PositiveIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"

class EnrollmentOfficerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    office_number = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.user.username} - {self.department.name}"
