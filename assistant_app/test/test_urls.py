import pytest
from django.urls import reverse, resolve
from assistant_app import views

@pytest.mark.parametrize("url_name, kwargs, expected_view", [
    ("assistant_app:home", {}, views.home),
    ("assistant_app:about", {}, views.about),
    ("assistant_app:login", {}, views.login_view),
    ("assistant_app:register", {}, views.register_view),
    ("assistant_app:logout", {}, views.logout_view),
    ("assistant_app:account", {}, views.account_view),
    ("assistant_app:calculator", {}, views.calculator),
    ("assistant_app:courses", {}, views.courses),
    ("assistant_app:add_course", {}, views.add_course),
    ("assistant_app:all_grades", {}, views.grades),
    ("assistant_app:add_grade", {}, views.add_grade),
    ("assistant_app:all_assignments", {}, views.assignments),
    ("assistant_app:add_assignment", {}, views.add_assignment),
    ("assistant_app:ajax_get_assignments", {}, views.get_assignments),
    ("assistant_app:edit_course", {"course_slug": "test-slug"}, views.edit_course),
    ("assistant_app:delete_course", {"course_slug": "test-slug"}, views.delete_course),
    ("assistant_app:edit_grade", {"grade_id": 1}, views.edit_grade),
    ("assistant_app:delete_grade", {"grade_id": 1}, views.delete_grade),
    ("assistant_app:grades_for_course", {"course_slug": "test-slug"}, views.grades),
    ("assistant_app:add_grade_for_course", {"course_slug": "test-slug"}, views.add_grade),
    ("assistant_app:edit_grade_for_course", {"course_slug": "test-slug", "grade_id": 1}, views.edit_grade),
    ("assistant_app:delete_grade_for_course", {"course_slug": "test-slug", "grade_id": 1}, views.delete_grade),
    ("assistant_app:edit_assignment", {"assignment_id": 1}, views.edit_assignment),
    ("assistant_app:delete_assignment", {"assignment_id": 1}, views.delete_assignment),
    ("assistant_app:assignments_for_course", {"course_slug": "test-slug"}, views.assignments),
    ("assistant_app:add_assignment_for_course", {"course_slug": "test-slug"}, views.add_assignment),
    ("assistant_app:edit_assignment_for_course", {"course_slug": "test-slug", "assignment_id": 1}, views.edit_assignment),
    ("assistant_app:delete_assignment_for_course", {"course_slug": "test-slug", "assignment_id": 1}, views.delete_assignment),
    ("assistant_app:ajax_assignment_complete", {"assignment_id": 1}, views.mark_assignment_complete),
])

def test_url_resolves(url_name, kwargs, expected_view):
    url = reverse(url_name, kwargs=kwargs)
    resolver = resolve(url)
    assert resolver.func.__name__ == expected_view.__name__
