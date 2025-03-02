from django.urls import path
from assistant_app import views

app_name = 'assistant_app'

urlpatterns = [
    path("", views.home, name="home"),
]
