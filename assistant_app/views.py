from django.shortcuts import get_object_or_404, render
from django.db.models import Sum, F, ExpressionWrapper, FloatField, Count, Q, Avg
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

@login_required
def courses(request):
    # Query to get all courses for the user and calculate the average grade using weights
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
        average_grade = course_grades.aggregate(
            total_weighted_grades=Sum(F('grade') * F('credits'), output_field=FloatField()),
            total_credits=Sum('credits', output_field=FloatField())
        )
        if average_grade['total_credits']:
            course_average = average_grade['total_weighted_grades'] / average_grade['total_credits']
        else:
            course_average = None

        return render(request, 'assistant_app/grades.html', {
            'course_slug': course_slug,
            'course': course,
            'course_grades': course_grades,
            'course_average_grade': course_average,
            'all_grades_view': False
        })
    
    else:
        grades_exist = False
        grades_by_course = {}
        courses = Course.objects.filter(user=request.user)
        average_grade = Grade.objects.filter(course__user=request.user).aggregate(
                                total_weighted_grades=Sum(F('grade') * F('credits'), output_field=FloatField()),
                                total_credits=Sum('credits', output_field=FloatField())
                                )
        if average_grade['total_credits']:
            overall_average = average_grade['total_weighted_grades'] / average_grade['total_credits']
        else:
            overall_average = None
        
        for course in courses:
            if course.grades.exists():
                grades_exist = True
                break

        if grades_exist:
            for course in courses:
                grades_by_course[course] = Grade.objects.filter(course=course)

        return render(request, 'assistant_app/grades.html', {
            'grades_by_course': grades_by_course,
            'overall_average_grade': overall_average,
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
                assignment.save()

            if not course_slug:
                return redirect('assistant_app:all_grades')
            
            return redirect('assistant_app:grades_for_course', course_slug=course.course_slug if course else form.cleaned_data['course'].course_slug)
    else:
        form = GradeForm(user=request.user, course_slug=course_slug)

    return render(request, "assistant_app/add_grade.html", {"form": form, "course": course})

@login_required
def edit_grade(request, grade_id, course_slug=None):
    grade = get_object_or_404(Grade, id=grade_id)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade, user=request.user, course_slug=course_slug)
        if form.is_valid():
            new_grade = form.save(commit=False)
            new_grade.course = grade.course
            new_grade.save()
        if not course_slug:
            return redirect('assistant_app:all_grades')
        return redirect('assistant_app:grades_for_course', course_slug=grade.course.course_slug)
    else:
        form = GradeForm(instance=grade, user=request.user, course_slug=course_slug)

    return render(request, 'assistant_app/edit_grade.html', {"form": form, "grade": grade, "course_slug": course_slug})


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
        course_assignments_pending = Assignment.objects.filter(course=course, is_done=False)
        course_assignments_completed = Assignment.objects.filter(course=course, is_done=True)
        due_assignments = Assignment.objects.filter(course=course, is_done=False).count()

        return render(request, 'assistant_app/assignments.html', {
            'course_slug': course_slug,
            'course': course,
            'course_assignments_pending': course_assignments_pending,
            'course_assignments_completed': course_assignments_completed,
            'course_due_assignments': due_assignments,
            'all_assignments_view': False
        })
    
    else:
        assignments_exists = False
        assignments_by_course = {}
        completed_assignments = []
        courses = Course.objects.filter(user=request.user)
        due_assignments = Assignment.objects.filter(course__user=request.user, is_done=False).count()

        for course in courses:
            if course.assignments.exists():
                assignments_exists = True
                break
        
        if assignments_exists:
            for course in courses:
                assignments_by_course[course] = Assignment.objects.filter(course=course, is_done=False)
                completed_assignments.extend(Assignment.objects.filter(course=course, is_done=True))

        return render(request, 'assistant_app/assignments.html', {
            'assignments_by_course': assignments_by_course,
            'completed_assignments' : completed_assignments,
            'overall_due_assignments': due_assignments,
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
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment, user=request.user, course_slug=course_slug)
        if form.is_valid():
            new_assignment = form.save(commit=False)
            new_assignment.course = assignment.course
            if new_assignment.graded == False:
                new_assignment.grade = None
            new_assignment.save()
        if not course_slug:
            return redirect('assistant_app:all_assignments')
        return redirect('assistant_app:assignments_for_course', course_slug=assignment.course.course_slug)
    else:
        form = AssignmentForm(instance=assignment, user=request.user, course_slug=course_slug)

    return render(request, 'assistant_app/edit_assignment.html', {"form": form, "assignment": assignment, "course_slug": course_slug})

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

@login_required
def mark_assignment_complete(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, course__user=request.user)
    assignment.is_done = not assignment.is_done  # Toggle the status
    assignment.save()
    return JsonResponse({'status': 'success', 'is_done': assignment.is_done})
