from django.contrib import admin
from assistant_app.models import *

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'user')  # Display ID, Name, and User
    search_fields = ('course_name',)  # Allow searching by course name

class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'grade', 'date')  # Display ID, Course, Grade, Date
    search_fields = ('course__course_name',)  # Search by course name
    

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'name', 'is_done', 'deadline')  # Display ID, Course, Name, Completion Status, Deadline
    list_filter = ('is_done', 'deadline')  # Filter by completion and deadline
    search_fields = ('name', 'course__course_name')  # Search by assignment name or course


# Register models with customised admin views
admin.site.register(Course, CourseAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Assignment, AssignmentAdmin)