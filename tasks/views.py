from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def hello_world(request):
    title = 'Hello world'
    return render(request, 'signup.html', {
        'title': title,
        'form': UserCreationForm
    })
