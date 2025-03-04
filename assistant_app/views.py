from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CalculatorForm
from django.contrib.auth.decorators import login_required

def home(request):
    context_dict = {"title": "Welcome to the Student Assistant App",
                    "message": "Hello, world!",}
    
    return render(request, "assistant_app/home.html", context=context_dict)

@login_required
def about(request):
    return render(request, "assistant_app/about.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('assistant_app:home')
        else:
            return render(request, 'assistant_app/login.html', {'error': 'Invalid credentials'})

    return render(request, 'assistant_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('assistant_app:home')
    else:
        form = RegistrationForm()
    return render(request, 'assistant_app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('assistant_app:login')

@login_required
def account_view(request):
    return render(request, 'assistant_app/account.html')

def calculator(request):
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            assignment = form.cleaned_data['assignment']
            grade = form.cleaned_data['grade']
            weight = form.cleaned_data['weight']
            result = grade * weight
        return render(request, 'assistant_app/calculator.html', {'form': form, 'result': result})
    else:
        form = CalculatorForm()
    return render(request, 'assistant_app/calculator.html', {'form': form})


"""This is a dummy thing to test the courses. Need to delete once we have the models ready"""
class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name

courses_list = [
    Course(0, "ADS2 2007"),
    Course(1, "WAD 2021"),
    Course(2, "OOSE 2008"),
]

@login_required
def courses(request):
    return render(request, 'assistant_app/courses.html', {'courses': courses_list})

@login_required
def add_course(request):
    return render(request, 'assistant_app/add_course.html')

@login_required
def edit_course(request, course_id):
    return render(request, 'assistant_app/edit_course.html', {'course_id': course_id})

@login_required
def delete_course(request, course_id):
    """Need to edit the logic when we start using the models"""
    global courses_list
    course_to_delete = None
    for course in courses_list:
        if course.id == course_id:
            course_to_delete = course
            break
    if course_to_delete:
        courses_list.remove(course_to_delete)

    return redirect('assistant_app:courses')

@login_required
def deadlines(request):
    return render(request, 'assistant_app/deadlines.html')

@login_required
def add_deadline(request):
    return render(request, 'assistant_app/add_deadline.html')

@login_required
def edit_deadline(request, deadline_id):
    return render(request, 'assistant_app/edit_deadline.html', {'deadline_id': deadline_id})

@login_required
def grades(request):
    return render(request, 'assistant_app/grades.html')

@login_required
def add_grade(request):
    return render(request, 'assistant_app/add_grade.html')

@login_required
def edit_grade(request, grade_id):
    return render(request, 'assistant_app/edit_grade.html', {'grade_id': grade_id})