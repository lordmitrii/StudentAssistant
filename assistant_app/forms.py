from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
