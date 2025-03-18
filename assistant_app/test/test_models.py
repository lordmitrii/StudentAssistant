from django.test import TestCase
from django.contrib.auth.models import User
from assistant_app.models import Course, Grade, Assignment
from django.utils.text import slugify
from django.utils.timezone import now

class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(user=self.user, course_name="Mathematics")

    def test_course_creation(self):
        self.assertEqual(self.course.course_name, "Mathematics")
        self.assertEqual(self.course.user.username, "testuser")
        self.assertTrue(self.course.course_slug.startswith("mathematics"))

    def test_slug_uniqueness(self):
        course2 = Course.objects.create(user=self.user, course_name="Mathematics")
        self.assertNotEqual(self.course.course_slug, course2.course_slug)

    def test_str_method(self):
        self.assertEqual(str(self.course), f"Mathematics")


class GradeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(user=self.user, course_name="Physics")
        self.grade = Grade.objects.create(course=self.course, grade=85.5, date=now(), note="Good job!")

    def test_grade_creation(self):
        self.assertEqual(self.grade.course.course_name, "Physics")
        self.assertEqual(self.grade.grade, 85.5)
        self.assertEqual(self.grade.note, "Good job!")

    def test_str_method(self):
        self.assertIn(str(self.grade.grade), str(self.grade))
        self.assertIn(self.grade.date.strftime('%d/%m/%Y'), str(self.grade))


class AssignmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(user=self.user, course_name="Biology")
        self.grade = Grade.objects.create(course=self.course, grade=90.0, date=now(), note="Well done!")
        self.assignment = Assignment.objects.create(
            course=self.course,
            grade=self.grade,
            graded=True,
            deadline=now(),
            is_done=True,
            name="Lab Report",
            note="Submit before 5 PM"
        )

    def test_assignment_creation(self):
        self.assertEqual(self.assignment.course.course_name, "Biology")
        self.assertEqual(self.assignment.name, "Lab Report")
        self.assertEqual(self.assignment.note, "Submit before 5 PM")
        self.assertTrue(self.assignment.graded)
        self.assertTrue(self.assignment.is_done)

    def test_assignment_str_method(self):
        self.assertEqual(str(self.assignment), "Lab Report")

    def test_assignment_ordering(self):
        assignment2 = Assignment.objects.create(
            course=self.course,
            deadline=now(),
            name="Homework"
        )
        assignments = list(Assignment.objects.all())
        self.assertLessEqual(assignments[0].deadline, assignments[1].deadline) 
