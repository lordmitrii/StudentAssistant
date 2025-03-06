from django.db import models
from django.contrib.auth.models import User # use the built-in User model for authentication


class Course(models.Model):
    """
    Course model representing academic courses a student is taking.
    Each course belongs to a specific user and can have multiple assignments.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.course_name


class Grade(models.Model):
    """
    Grade model representing a grade received for an assignment.
    Each grade belongs to a user and has optional notes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    grade = models.FloatField()
    date = models.DateTimeField()
    note = models.CharField(max_length=256, blank=True)
    
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
    note = models.CharField(max_length=256, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['deadline']

