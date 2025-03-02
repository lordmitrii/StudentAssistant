from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context_dict = {"title": "Welcome to the Student Assistant App",
                "message": "Hello, world!",}
    
    return render(request, "assistant_app/home.html", context=context_dict)