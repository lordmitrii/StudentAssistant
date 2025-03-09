from django.db import models
from django.contrib.auth.models import User # use the built-in User model for authentication
from django.utils.text import slugify


class Course(models.Model):
    """
    Course model representing academic courses a student is taking.
    Each course belongs to a specific user and can have multiple assignments and courses.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=50)
    course_slug = models.SlugField(max_length=60)

    class Meta:
        unique_together = ('user', 'course_slug')  # Slug uniqueness per user

    def save(self, *args, **kwargs):
        if not self.course_slug:
            base_slug = slugify(self.course_name)
            slug = base_slug
            counter = 1
            while Course.objects.filter(user=self.user, course_slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.course_slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name
    


class Grade(models.Model):
    """
    Grade model representing a grade received for an assignment or manually added.
    Each grade belongs to a course and has optional notes.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    grade = models.FloatField()
    credits = models.IntegerField(default=10)
    date = models.DateTimeField()
    note = models.CharField(max_length=256, blank=True)

    
    def __str__(self):
        return f"{self.grade} - {self.date.strftime('%d/%m/%Y')}"


class Assignment(models.Model):
    """
    Assignment model representing academic tasks with deadlines.
    Each assignment belongs to a course and may have an associated grade.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    grade = models.OneToOneField(Grade, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignment')
    graded = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    name = models.CharField(max_length=25)
    note = models.CharField(max_length=256, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['deadline']
