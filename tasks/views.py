from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, CreateView
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task


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
                login(request, new_user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User name already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })


class TaskView(ListView):
    model = Task
    template_name = "tasks.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


def create_task(request):
    if (request.method == 'GET'):
        return render(request, 'create_task.html', {
            'form': CreateTaskForm
        })
    elif (request.method == 'POST'):
        try:
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request, 'create_task.html', {
                'form': CreateTaskForm,
                'error': 'Please provide valid data'
            })


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
