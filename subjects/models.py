from django.db import models
from accounts.models import Department

class Subject(models.Model):
    SUBJECT_TYPE_CHOICES = (
        ('MAJOR', 'Major'),
        ('MINOR', 'Minor'),
    )
    YEAR_LEVEL_CHOICES = (
         (1, '1st Year'),
         (2, '2nd Year'),
         (3, '3rd Year'),
         (4, '4th Year'),
    )
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="subjects")
    subject_type = models.CharField(max_length=10, choices=SUBJECT_TYPE_CHOICES)
    year_level = models.PositiveIntegerField(choices=YEAR_LEVEL_CHOICES, null=True, blank=True, help_text="Applicable for major subjects only")
    prerequisites = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='dependent_subjects',
        help_text="Select prerequisite subjects (if any)"
    )
    units = models.PositiveIntegerField(default=3)
    description = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
