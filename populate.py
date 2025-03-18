import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_assistant.settings")
django.setup()

from django.contrib.auth.models import User
from assistant_app.models import Course, Grade, Assignment, News
from django.utils.text import slugify

def populate():
    # Create or get a test user
    user, created = User.objects.get_or_create(username="testuser", email="test@example.com")
    user.set_password("password")
    user.save()

    # Sample course names
    course_names = ["MATHS2", "WAD2", "ADS2", "OOSE2", "CS1S"]

    # Create courses with unique slugs
    courses = []
    for name in course_names:
        slug = slugify(name)
        course, created = Course.objects.get_or_create(user=user, course_name=name, course_slug=slug)
        courses.append(course)

    # Create grades and assignments for each course
    for course in courses:
        for _ in range(3):  # Create 3 grades per course
            grade_value = round(random.uniform(50, 100), 2)
            grade_date = timezone.now() - timedelta(days=random.randint(1, 30))
            grade = Grade.objects.create(
                course=course,
                grade=grade_value,
                credits=random.choice([5, 10]),
                date=grade_date,
                note="Sample grade entry"
            )

            assignment = Assignment.objects.create(
                course=course,
                grade=grade if random.choice([True, False]) else None,
                graded=random.choice([True, False]),
                deadline=timezone.now() + timedelta(days=random.randint(5, 20)),
                is_done=random.choice([True, False]),
                name=f"Assignment {random.randint(1, 10)}",
                note="Sample assignment entry"
            )

    # Create sample news entries
    for i in range(3):
        News.objects.create(
            title=f"News Title {i+1}",
            content=f"This is the content of news {i+1}.",
            is_published=True
        )

    print("Database successfully populated with sample data.")

if __name__ == "__main__":
    populate()
