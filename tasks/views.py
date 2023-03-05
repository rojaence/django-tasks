from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if (request.method == 'GET'):
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    if (request.method == 'POST'):
        if request.POST['password1'] == request.POST['password2']:
            # Register user
            try:
                new_user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                new_user.save()
                return HttpResponse('User created successfully')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User name already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })
