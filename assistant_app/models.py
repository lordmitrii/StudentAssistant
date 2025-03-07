from django.db import models
from django.contrib.auth.models import User # use the built-in User model for authentication

"""
For reference:
Django's built-in User model includes:
Username
Password
Email
First and last name
Administrative flags (is_staff, is_active, etc.)
Authentication methods
"""

class Course(models.Model):
    """
    Course model representing academic courses a student is taking.
    Each course belongs to a specific user and can have multiple assignments.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=50)
    credit_hours = models.DecimalField(max_digits=3, decimal_places=1, default=3.0)
    
    def __str__(self):
        return self.course_name


class Grade(models.Model):
    """
    Grade model representing a grade received for an assignment or manually added.
    Each grade belongs to a user and has optional notes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades', null=True, blank=True)
    grade = models.FloatField()
    weight = models.FloatField(default=1.0)
    date = models.DateTimeField()
    note = models.CharField(max_length=256, blank=True)
    is_manual = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.grade} - {self.date.strftime('%Y-%m-%d')}"


class Assignment(models.Model):
    """
    Assignment model representing academic tasks with deadlines.
    Each assignment belongs to a course and may have an associated grade.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    grade = models.OneToOneField(Grade, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignment')
    graded = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    name = models.CharField(max_length=25)
    weight = models.FloatField(default=1.0)
    note = models.CharField(max_length=256, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['deadline']

