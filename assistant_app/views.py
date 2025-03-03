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

def calculator_view(request):
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

@login_required
def courses_view(request):
    courses_dict = [{"name": "ADS2 2007"},
                    {"name": "WAD 2021"},
                    {"name": "OOSE 2008"}]
    
    return render(request, 'assistant_app/courses.html', {'courses': courses_dict})
