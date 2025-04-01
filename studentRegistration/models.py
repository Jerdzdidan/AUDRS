from django.db import models
from accounts.models import StudentProfile

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

class StudentRegistration(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="registrations"
    )
    preferred_section = models.CharField(
        max_length=20,
        choices=(
            ('Section A', 'Section A'),
            ('Section B', 'Section B'),
            ('Section C', 'Section C'),
        ),
        default='Section A',
        help_text="Student's preferred section"
    )
    preferred_time_start = models.TimeField(help_text="Preferred start time for classes")
    preferred_time_end = models.TimeField(help_text="Preferred end time for classes")
    
    preferred_class_days = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma-separated list of preferred class days (e.g., Monday,Thursday,Saturday)"
    )
    
    selected_minor_subjects = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma-separated list of selected minor subject IDs"
    )
    additional_comments = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional information provided by the student"
    )
    
    registration_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(
        default=False,
        help_text="Indicates if the registration process is completed"
    )
    
    registration_form_image = models.ImageField(
        upload_to='registration_forms/',
        blank=True,
        null=True,
        help_text="Final registration form image uploaded by the officer"
    )
    
    submitted = models.BooleanField(
        default=False,
        help_text="Indicates if the registration form has been submitted by the student"
    )
    
    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"Registration for {self.student.user.get_full_name()} ({self.student.student_id}) - {status}"


class RegistrationWindow(models.Model):
    start_date = models.DateField(help_text="When registration starts (Date only)")
    start_time = models.TimeField(help_text="When registration starts (Time only)")
    end_date = models.DateField(help_text="When registration ends (Date only)")
    end_time = models.TimeField(help_text="When registration ends (Time only)")
    is_open = models.BooleanField(default=False, help_text="Indicates if registration is currently open")

    def __str__(self):
        status = "Open" if self.is_open else "Closed"
        return (
            f"Registration Window ({status}): "
            f"{self.start_date:%b. %d, %Y} {self.start_time:%I:%M:%S%p} to "
            f"{self.end_date:%b. %d, %Y} {self.end_time:%I:%M:%S%p}"
        )