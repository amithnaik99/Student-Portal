
from django.db import models
from django.contrib.auth.models import User

# Student Profile — linked to Django's built-in User (for login)
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    dob = models.DateField(null=True, blank=True, help_text="Format: YYYY-MM-DD")
    def __str__(self):
        return f"{self.name} ({self.usn})"


# Announcements / Notices posted by admin
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


# Attendance — per student, per subject
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    percentage = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}: {self.percentage}%"


# Internal Marks — per student, per subject
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}: {self.marks}"


# Timetable — day, subject, time slot
class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    subject = models.CharField(max_length=100)
    time = models.CharField(max_length=50)  # e.g. "9:00 AM - 10:00 AM"

    def __str__(self):
        return f"{self.day} | {self.subject} | {self.time}"