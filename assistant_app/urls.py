from django.urls import path
from assistant_app import views

app_name = 'assistant_app'

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),

    path("login/", views.login_view, name="login"),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),

    path('calculator/', views.calculator, name='calculator'),

    path('courses/', views.courses, name='courses'),
    path('courses/add', views.add_course, name='add_course'),
    path('courses/<int:course_id>/edit', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete', views.delete_course, name='delete_course'),
    
    path('courses/grades', views.grades, name='grades'),
    path('courses/grades/add', views.add_grade, name='add_grade'),
    path('courses/grades/<int:course_id>/edit', views.edit_grade, name='edit_grade'),

    path('courses/deadlines', views.deadlines, name='deadlines'),
    path('courses/deadlines/add', views.add_deadline, name='add_deadline'),
    path('courses/deadlines/<int:course_id>/edit', views.edit_deadline, name='edit_deadline'),
]
