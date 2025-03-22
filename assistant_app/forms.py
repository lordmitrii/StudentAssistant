from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Grade, Assignment
from django.utils.timezone import now

# Registration form for new users
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# Course form for creating and updating courses
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


# Grade form for creating and updating grades
class GradeForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label="Course")
    assignment = forms.ModelChoiceField(queryset=Assignment.objects.none(), required=False, label="Assignment")

    class Meta:
        model = Grade
        fields = ['course', 'assignment', 'grade', 'credits', 'date', 'note']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add any relevant notes'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter grades in percentage', 'min': 0, 'max': 100}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        course_slug = kwargs.pop('course_slug', None)
        super().__init__(*args, **kwargs)
        
        self.fields['date'].initial = now()
        
        # If a course is provided, hide the course field
        if course_slug:
            course = Course.objects.get(course_slug=course_slug, user=user)
            self.fields.pop('course')  # Remove course field since its already selected
            self.fields['assignment'].queryset = Assignment.objects.filter(course=course, graded=True, grade=None)
            if not self.fields['assignment'].queryset.exists():
                self.fields['assignment'].empty_label = "No Assignments Available"
            else:
                self.fields['assignment'].empty_label = "Select Assignment (Optional)"
        else:
            self.fields['course'].queryset = Course.objects.filter(user=user)
            self.fields['assignment'].widget.attrs.update({'class': 'form-control'})
            self.fields['course'].widget.attrs.update({'class': 'form-control'})

            # Dynamically update the queryset for assignments so that we dont get errors on saving
            if self.data.get('course'):
                try:
                    course_id = int(self.data.get('course'))
                    self.fields['assignment'].queryset = Assignment.objects.filter(course_id=course_id)
                except (ValueError, TypeError):
                    self.fields['assignment'].queryset = Assignment.objects.none()
            else:
                self.fields['assignment'].queryset = Assignment.objects.none()

    # Validate that the selected assignment belongs to the selected course
    def clean_assignment(self):
        assignment = self.cleaned_data.get("assignment")
        course = self.cleaned_data.get("course")

        if assignment and course and assignment.course_id != course.id:
            raise forms.ValidationError("The selected assignment does not belong to the chosen course.")
        
        return assignment

# Assignment form for creating and updating assignments
class AssignmentForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label="Course")

    class Meta:
        model = Assignment
        fields = ['course', 'name', 'graded', 'deadline', 'note']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'graded': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter assignment name'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add any relevant notes'}),
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


# These fields are used in the admin interface to display the course and assignment names along with the user who created them.
class CourseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.course_name} (User: {obj.user.username})"

class AssignmentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} - {obj.course.course_name} (User: {obj.course.user.username})"

class GradeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"Grade: {obj.grade} ({obj.course.course_name} - {obj.course.user.username})"

class AssignmentAdminForm(forms.ModelForm):
    course = CourseChoiceField(queryset=Course.objects.all())

    class Meta:
        model = Assignment
        fields = '__all__'

class GradeAdminForm(forms.ModelForm):
    course = CourseChoiceField(queryset=Course.objects.all())

    class Meta:
        model = Grade
        fields = '__all__'
