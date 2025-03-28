from django.db import models
from accounts.models import StudentProfile
from subjects.models import Subject

class StudentSubjectChecklist(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='subject_checklists'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='student_checklists'
    )
    taken = models.BooleanField(default=False, help_text="Indicates if the student has taken the subject.")
    taken_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'subject')
        verbose_name = "Student Subject Checklist"
        verbose_name_plural = "Student Subject Checklists"

    def __str__(self):
        status = "Taken" if self.taken else "Not Taken"
        return f"{self.student.user.username} - {self.subject.code} ({status})"