from django.db import models

# Create your models here.
from django.db import models
from accounts.models import Department, EnrollmentOfficerProfile

class Subject(models.Model):
    SUBJECT_TYPE_CHOICES = (
        ('MAJOR', 'Major'),
        ('MINOR', 'Minor'),
    )
    
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    subject_type = models.CharField(max_length=10, choices=SUBJECT_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    lec_units = models.PositiveIntegerField(default=3)
    lab_units = models.PositiveIntegerField(default=0)
    total_units = models.PositiveIntegerField(default=3)  
    pre_requisite = models.CharField(max_length=100, blank=True, null=True)
    approved = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(
        EnrollmentOfficerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submitted_subjects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"