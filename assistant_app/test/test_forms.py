from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

from assistant_app.forms import (
    RegistrationForm, CourseForm, GradeForm, AssignmentForm
)
from assistant_app.models import Course, Assignment


class RegistrationFormTests(TestCase):
    def test_registration_form_valid(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())

    def test_registration_form_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass123!',
        }
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)



class CourseFormTests(TestCase):
    def test_course_form_valid(self):
        data = {
            'course_name': 'Test Course',
        }
        form = CourseForm(data)
        self.assertTrue(form.is_valid())


class GradeFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(user=self.user, course_name='Test Course')
        self.assignment = Assignment.objects.create(
            course=self.course,
            name="Assignment 1",
            graded=True,
            deadline=now() + timedelta(days=1)
        )

    def test_grade_form_with_course_slug(self):
        data = {
            'grade': 90,
            'credits': 5,
            'date': now().strftime("%Y-%m-%d %H:%M:%S"),
            'note': 'Great work',
            'assignment': self.assignment.id,  # 选择作业
        }
        form = GradeForm(data, user=self.user, course_slug=self.course.course_slug)
        self.assertTrue(form.is_valid())
        self.assertNotIn('course', form.fields)
        qs = form.fields['assignment'].queryset
        self.assertIn(self.assignment, qs)

    def test_grade_form_without_course_slug(self):
        data = {
            'course': self.course.id,
            'grade': 85,
            'credits': 3,
            'date': now().strftime("%Y-%m-%d %H:%M:%S"),
            'note': 'Good job',
        }
        form = GradeForm(data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertIn('course', form.fields)
        qs = form.fields['assignment'].queryset
        self.assertEqual(qs.count(), 1)
        self.assertIn(self.assignment, qs)

    def test_clean_assignment_validation(self):
        other_course = Course.objects.create(user=self.user, course_name='Other Course')
        other_assignment = Assignment.objects.create(
            course=other_course,
            name="Other Assignment",
            graded=True,
            deadline=now() + timedelta(days=1)
        )
        data = {
            'course': self.course.id,
            'grade': 80,
            'credits': 2,
            'date': now().strftime("%Y-%m-%d %H:%M:%S"),
            'note': '',
            'assignment': other_assignment.id,
        }
        form = GradeForm(data, user=self.user)
        self.assertFalse(form.is_valid())
        expected_error = "Select a valid choice. That choice is not one of the available choices."
        self.assertIn(expected_error, form.errors.get("assignment", []))


class AssignmentFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(user=self.user, course_name='Test Course')

    def test_assignment_form_with_course_slug(self):
        data = {
            'name': 'Assignment 1',
            'graded': False,
            'deadline': (now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            'note': 'Test note',
        }
        form = AssignmentForm(data, user=self.user, course_slug=self.course.course_slug)
        self.assertTrue(form.is_valid())
        self.assertNotIn('course', form.fields)

    def test_assignment_form_without_course_slug(self):
        data = {
            'course': self.course.id,
            'name': 'Assignment 2',
            'graded': True,
            'deadline': (now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            'note': 'Test note 2',
        }
        form = AssignmentForm(data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertIn('course', form.fields)
        qs = form.fields['course'].queryset
        self.assertIn(self.course, qs)
