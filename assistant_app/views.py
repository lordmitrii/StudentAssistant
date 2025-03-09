from django.shortcuts import get_object_or_404, render
from django.db.models import Sum, F, ExpressionWrapper, FloatField, Count, Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CalculatorForm, CourseForm, GradeForm, AssignmentForm
from django.contrib.auth.decorators import login_required
from .models import Course, Grade, Assignment

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
            credits = form.cleaned_data['credits']
            result = grade * credits
        return render(request, 'assistant_app/calculator.html', {'form': form, 'result': result})
    else:
        form = CalculatorForm()
    return render(request, 'assistant_app/calculator.html', {'form': form})


def courses(request):
    # Query to get all courses for the logged-in user and calculate the average grade using weights
    courses = Course.objects.filter(user=request.user).annotate(
        total_weighted_grades=Sum(F('grades__grade') * F('grades__credits'), output_field=FloatField()),
        total_credits=Sum('grades__credits', output_field=FloatField()),
        due_assignments=Count('assignments', filter=Q(assignments__is_done=False), distinct=True)
    ).annotate(
        average_grade=ExpressionWrapper((F('total_weighted_grades') / F('total_credits')), output_field=FloatField())
    )

    return render(request, 'assistant_app/courses.html', {'courses': courses})

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = request.user
            new_course.save()
            return redirect('assistant_app:courses')
    else:
        form = CourseForm()
    return render(request, 'assistant_app/add_course.html', {'form': form})

@login_required
def edit_course(request, course_slug):
    course = get_object_or_404(Course, course_slug=course_slug, user=request.user)
    original_name = course.course_name
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            updated_course = form.save(commit=False)
            # If the course name has changed, reset the slug
            if original_name.lower() != updated_course.course_name.lower():
                updated_course.course_slug = None
            updated_course.save()
            return redirect('assistant_app:courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'assistant_app/edit_course.html', {'form': form, 'course': course})


@login_required
def delete_course(request, course_slug):
    course = get_object_or_404(Course, course_slug=course_slug, user=request.user)
    course.delete()
    return redirect('assistant_app:courses')


@login_required
def grades(request, course_slug=None):
    if course_slug:
        course = get_object_or_404(Course, course_slug=course_slug, user=request.user)
        course_grades = Grade.objects.filter(course=course)
        return render(request, 'assistant_app/grades.html', {
            'course_slug': course_slug,
            'course': course,
            'course_grades': course_grades,
            'all_grades_view': False
        })
    
    else:
        courses = Course.objects.filter(user=request.user)
        grades_by_course = {course: Grade.objects.filter(course=course) for course in courses}

        return render(request, 'assistant_app/grades.html', {
            'grades_by_course': grades_by_course,
            'all_grades_view': True
        })


@login_required
def add_grade(request, course_slug=None):
    course = None
    if course_slug:
        course = get_object_or_404(Course, course_slug=course_slug, user=request.user)

    if request.method == "POST":
        form = GradeForm(request.POST, user=request.user, course_slug=course_slug)
        if form.is_valid():
            grade = form.save(commit=False)
            if course:
                grade.course = course
            grade.save()
            assignment = form.cleaned_data.get('assignment')
            if assignment:
                assignment.grade = grade
                assignment.graded = True
                assignment.save()

            if not course_slug:
                return redirect('assistant_app:all_grades')
            
            return redirect('assistant_app:grades_for_course', course_slug=course.course_slug if course else form.cleaned_data['course'].course_slug)
    else:
        form = GradeForm(user=request.user, course_slug=course_slug)

    return render(request, "assistant_app/add_grade.html", {"form": form, "course": course})

@login_required
def edit_grade(request, grade_id, course_slug=None):
    return render(request, 'assistant_app/edit_grade.html', {'grade_id': grade_id})

@login_required
def delete_grade(request, grade_id, course_slug=None):
    grade = get_object_or_404(Grade, id=grade_id)
    grade.delete()

    if course_slug:
        return redirect('assistant_app:grades_for_course', course_slug=course_slug)
    else:
        return redirect('assistant_app:all_grades')

@login_required
def assignments(request, course_slug=None):
    if course_slug:
        course = get_object_or_404(Course, course_slug=course_slug, user=request.user)
        course_assignments = Assignment.objects.filter(course=course)
        return render(request, 'assistant_app/assignments.html', {
            'course_slug': course_slug,
            'course': course,
            'course_assignments': course_assignments,
            'all_assignments_view': False
        })
    
    else:
        courses = Course.objects.filter(user=request.user)
        assignments_by_course = {course: Assignment.objects.filter(course=course) for course in courses}

        return render(request, 'assistant_app/assignments.html', {
            'assignments_by_course': assignments_by_course,
            'all_assignments_view': True
        })

@login_required
def add_assignment(request, course_slug=None):
    course = None
    if course_slug:
        course = get_object_or_404(Course, course_slug=course_slug, user=request.user)

    if request.method == "POST":
        form = AssignmentForm(request.POST, user=request.user, course_slug=course_slug)
        if form.is_valid():
            assignment = form.save(commit=False)
            if course:
                assignment.course = course
            assignment.save()

            if not course_slug:
                return redirect('assistant_app:all_assignments')
            
            return redirect('assistant_app:assignments_for_course', course_slug=course.course_slug if course else form.cleaned_data['course'].course_slug)
    else:
        form = AssignmentForm(user=request.user, course_slug=course_slug)

    return render(request, "assistant_app/add_assignment.html", {"form": form, "course": course})

@login_required
def edit_assignment(request, assignment_id, course_slug=None):
    return render(request, 'assistant_app/edit_assignment.html', {'assignment_id': assignment_id})

@login_required
def delete_assignment(request, assignment_id, course_slug=None):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()

    if course_slug:
        return redirect('assistant_app:assignments_for_course', course_slug=course_slug)
    else:
        return redirect('assistant_app:all_assignments')
    
@login_required
def get_assignments(request):
    course_id = request.GET.get('course_id')
    assignments = Assignment.objects.filter(course_id=course_id, graded=True, grade=None).values('id', 'name')
    return JsonResponse({'assignments': list(assignments)})

