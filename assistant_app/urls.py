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

    path('calculator/', views.calculator_view, name='calculator'),
    path('courses/', views.courses_view, name='courses'),
]
