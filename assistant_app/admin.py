from django.contrib import admin
from .models import *
from .forms import AssignmentAdminForm, GradeAdminForm

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'user')  
    search_fields = ('course_name', 'user__username') 

class GradeAdmin(admin.ModelAdmin):
    form = GradeAdminForm  
    list_display = ('id', 'course', 'grade', 'date')  
    search_fields = ('course__course_name', 'course__user__username') 
    
class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentAdminForm  
    list_display = ('id', 'course', 'name', 'is_done', 'deadline')  
    search_fields = ('name', 'course__course_name', 'course__user__username') 

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_posted', 'is_published') 
    list_filter = ('is_published', 'date_posted')  
    search_fields = ('title', 'content')  

# Register models with customised admin views
admin.site.register(Course, CourseAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(News, NewsAdmin)