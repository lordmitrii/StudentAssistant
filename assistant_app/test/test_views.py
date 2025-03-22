from datetime import datetime, timedelta

import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now

from assistant_app.models import Course, Grade, Assignment
from assistant_app.views import account_view

@pytest.mark.django_db
def test_home_view(client):
    url = reverse('assistant_app:home')
    response = client.get(url)
    assert response.status_code == 200
    assert b"Welcome to the Student Assistant App" in response.content

@pytest.mark.django_db
def test_about_view(client):
    url = reverse('assistant_app:about')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('assistant_app:login')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_view_post_success(client):
    user = User.objects.create_user(username="testuser", password="password")
    url = reverse('assistant_app:login')
    response = client.post(url, {'username': 'testuser', 'password': 'password'})
    assert response.status_code == 302
    assert response.url == reverse('assistant_app:home')

@pytest.mark.django_db
def test_login_view_post_failure(client):
    url = reverse('assistant_app:login')
    response = client.post(url, {'username': 'nonexistent', 'password': 'wrong'})
    assert response.status_code == 200
    assert b"Invalid credentials" in response.content

@pytest.mark.django_db
def test_register_view_get(client):
    url = reverse('assistant_app:register')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_register_view_post(client):
    url = reverse('assistant_app:register')
    data = {
        'username': 'newuser',
        'password1': 'StrongPass123',
        'password2': 'StrongPass123'
    }
    response = client.post(url, data)
    assert response.status_code == 302 
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_logout_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    url = reverse('assistant_app:logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('assistant_app:login')

@pytest.mark.django_db
def test_account_view_requires_login(client):
    url = reverse('assistant_app:account')
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_calculator_get(client):
    url = reverse('assistant_app:calculator')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_calculator_post(client):
    data = {
        'assignment': 'Test Assignment',
        'grade': '85',
        'credits': '3'
    }
    url = reverse('assistant_app:calculator')
    response = client.post(url, data)
    assert response.status_code == 200
    assert b"255" in response.content

@pytest.mark.django_db
def test_courses_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    Course.objects.create(user=user, course_name="Mathematics")
    url = reverse('assistant_app:courses')
    response = client.get(url)
    assert response.status_code == 200
    assert b"Mathematics" in response.content

@pytest.mark.django_db
def test_add_course_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    url = reverse('assistant_app:add_course')
    data = {'course_name': 'Physics'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Course.objects.filter(course_name='Physics').exists()

@pytest.mark.django_db
def test_edit_course_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Chemistry")
    url = reverse('assistant_app:edit_course', args=[course.course_slug])
    data = {'course_name': 'Organic Chemistry'}  
    response = client.post(url, data)
    assert response.status_code == 302
    course.refresh_from_db()
    assert course.course_name == 'Organic Chemistry'

@pytest.mark.django_db
def test_delete_course_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="History")
    url = reverse('assistant_app:delete_course', args=[course.course_slug])
    response = client.post(url)
    assert response.status_code == 302
    assert not Course.objects.filter(id=course.id).exists()

@pytest.mark.django_db
def test_grades_view_with_course_slug(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Biology")
    Grade.objects.create(course=course, grade=92, date=now(), note="Good")
    url = reverse('assistant_app:grades_for_course', args=[course.course_slug])
    response = client.get(url)
    assert response.status_code == 200
    assert b"92" in response.content

@pytest.mark.django_db
def test_grades_view_without_course_slug(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Economics")
    Grade.objects.create(course=course, grade=88, date=now(), note="Average")
    url = reverse('assistant_app:all_grades')
    response = client.get(url)
    assert response.status_code == 200
    assert b"88" in response.content

@pytest.mark.django_db
def test_add_grade_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Philosophy")
    url = reverse('assistant_app:add_grade', args=[course.course_slug])
    data = {
        "grade": "95",
        "credits": "4",
        "date": now().strftime("%Y-%m-%d %H:%M:%S")
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Grade.objects.filter(course=course, grade=95).exists()

@pytest.mark.django_db
def test_edit_grade_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Art")
    grade = Grade.objects.create(course=course, grade=75, date=now(), note="Needs improvement")
    url = reverse('assistant_app:edit_grade', args=[grade.id, course.course_slug])
    data = {
        "grade": "80",
        "credits": "3",
        "date": now().strftime("%Y-%m-%d %H:%M:%S")
    }
    response = client.post(url, data)
    assert response.status_code == 302
    grade.refresh_from_db()
    assert grade.grade == 80

@pytest.mark.django_db
def test_delete_grade_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Music")
    grade = Grade.objects.create(course=course, grade=65, date=now(), note="Average")
    url = reverse('assistant_app:delete_grade', args=[grade.id, course.course_slug])
    response = client.post(url)
    assert response.status_code == 302
    assert not Grade.objects.filter(id=grade.id).exists()

@pytest.mark.django_db
def test_assignments_view_with_course_slug(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Geography")
    Assignment.objects.create(course=course, name="Essay", is_done=False)
    url = reverse('assistant_app:assignments_for_course', args=[course.course_slug])
    response = client.get(url)
    assert response.status_code == 200
    assert b"Essay" in response.content

@pytest.mark.django_db
def test_assignments_view_without_course_slug(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Literature")
    Assignment.objects.create(course=course, name="Book Report", is_done=True)
    url = reverse('assistant_app:all_assignments')
    response = client.get(url)
    assert response.status_code == 200
    assert b"Book Report" in response.content

@pytest.mark.django_db
def test_add_assignment_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Drama")
    url = reverse('assistant_app:add_assignment', args=[course.course_slug])
    data = {
        "name": "Monologue",
        "deadline": now().strftime("%Y-%m-%d %H:%M:%S")
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Assignment.objects.filter(course=course, name="Monologue").exists()

@pytest.mark.django_db
def test_edit_assignment_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Economics")
    assignment = Assignment.objects.create(course=course, name="Quiz", is_done=False)
    url = reverse('assistant_app:edit_assignment', args=[assignment.id, course.course_slug])
    data = {
        "name": "Final Quiz",
        "deadline": now().strftime("%Y-%m-%d %H:%M:%S"),
        "graded": "True"
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assignment.refresh_from_db()
    assert assignment.name == "Final Quiz"

@pytest.mark.django_db
def test_delete_assignment_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Philosophy")
    assignment = Assignment.objects.create(course=course, name="Essay", is_done=False)
    url = reverse('assistant_app:delete_assignment', args=[assignment.id, course.course_slug])
    response = client.post(url)
    assert response.status_code == 302
    assert not Assignment.objects.filter(id=assignment.id).exists()

@pytest.mark.django_db
def test_get_assignments_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="History")
    Assignment.objects.create(course=course, name="Term Paper", graded=True, is_done=False)
    url = reverse('assistant_app:get_assignments')
    response = client.get(url, {'course_id': course.id})
    assert response.status_code == 200
    data = response.json()
    assert "assignments" in data

@pytest.mark.django_db
def test_mark_assignment_complete_view(client):
    user = User.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    course = Course.objects.create(user=user, course_name="Geography")
    assignment = Assignment.objects.create(course=course, name="Map Analysis", is_done=False)
    url = reverse('assistant_app:mark_assignment_complete', args=[assignment.id])
    response = client.post(url)
    assignment.refresh_from_db()
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
    assert assignment.is_done is True