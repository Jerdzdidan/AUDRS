from django.db import models
from accounts.models import Department, CustomUser, Program

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
    programs = models.ManyToManyField(
        'accounts.Program',
        related_name="subjects",
        blank=True,
        help_text="Select programs for which this subject is offered"
    )
    subject_type = models.CharField(max_length=10, choices=SUBJECT_TYPE_CHOICES)
    year_level = models.PositiveIntegerField(
        choices=YEAR_LEVEL_CHOICES, 
        null=True, 
        blank=True, 
        help_text="Applicable for major subjects only"
    )
    prerequisites = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='dependent_subjects',
        help_text="Select prerequisite subjects (if any)"
    )
    units = models.PositiveIntegerField(default=3)
    description = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class StudentSubjectChecklist(models.Model):
    student = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'STUDENT'}, 
        related_name='subject_checklists'
    )
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        related_name='student_checklists'
    )
    taken = models.BooleanField(default=False)
    taken_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'subject')
    
    def __str__(self):
        status = "Taken" if self.taken else "Not Taken"
        return f"{self.student.username} - {self.subject.code} ({status})"
