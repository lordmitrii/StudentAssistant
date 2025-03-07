from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Grade, Assignment

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CalculatorForm(forms.Form):
    #Chooices of assignments:
    ASSIGNMENT_CHOICES = (
        ('1', 'Assignment 1'),
        ('2', 'Assignment 2'),
        ('3', 'Assignment 3'),
        ('4', 'Assignment 4'),
        ('5', 'Assignment 5'),
    )
    assignment = forms.ChoiceField(choices=ASSIGNMENT_CHOICES, label='Assignment')
    grade = forms.FloatField(label='Grade')
    weight = forms.FloatField(label='Weight')
    
    class Meta:
        fields = ("assignment", "grade", "weight")

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name']
        labels = {
            'course_name': 'Course Name',
        }
        widgets = {
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),
        }

from django import forms
from .models import Grade, Course

class GradeForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label="Course")
    assignment = forms.ModelChoiceField(queryset=Assignment.objects.none(), required=False, label="Assignment")

    class Meta:
        model = Grade
        fields = ['course', 'assignment', 'grade', 'date', 'note']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        course_slug = kwargs.pop('course_slug', None)
        super().__init__(*args, **kwargs)

        # If a course is provided, hide the course field
        if course_slug:
            course = Course.objects.get(course_slug=course_slug, user=user)
            self.fields.pop('course')  # Remove course field since its already selected
            self.fields['assignment'].queryset = Assignment.objects.filter(course=course, graded=True)
            if not self.fields['assignment'].queryset.exists():
                self.fields['assignment'].empty_label = "No Assignments Available"
            else:
                self.fields['assignment'].empty_label = "Select Assignment (Optional)"
        else:
            self.fields['course'].queryset = Course.objects.filter(user=user)
            self.fields['assignment'].widget.attrs.update({'class': 'form-control'})
            self.fields['course'].widget.attrs.update({'class': 'form-control'})

            # If no assignments exist for the selected course, show 
            if self.data.get('course'):
                try:
                    course_id = int(self.data.get('course'))
                    self.fields['assignment'].queryset = Assignment.objects.filter(course_id=course_id)
                except (ValueError, TypeError):
                    self.fields['assignment'].queryset = Assignment.objects.none()
            else:
                self.fields['assignment'].queryset = Assignment.objects.none()


    

class AssignmentForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label="Course")

    class Meta:
        model = Assignment
        fields = ['course', 'name', "graded", 'deadline', 'note']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        course_slug = kwargs.pop('course_slug', None)
        super().__init__(*args, **kwargs)

        # If a course is provided, hide the course field
        if course_slug:
            self.fields.pop('course')  # Remove course field since its already selected
        else:
            self.fields['course'].queryset = Course.objects.filter(user=user)
            self.fields['course'].widget.attrs.update({'class': 'form-control'})




