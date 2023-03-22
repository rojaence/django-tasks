from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.db import IntegrityError
from django.utils import timezone
from .forms import CreateTaskForm, UpdateTaskForm
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


@method_decorator(login_required, name='dispatch')
class TaskView(ListView):
    model = Task
    template_name = "tasks.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        completed = self.request.GET.get('completed', None)
        if completed is not None:
            completed = completed.lower()
            if completed == 'true':
                return Task.objects.filter(user=self.request.user, completed=True)
            else:
                return Task.objects.filter(user=self.request.user, completed=False)
        else:
            return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completed = self.request.GET.get('completed', 'all')
        completed = completed.lower()
        if completed not in ['true', 'false']:
            context['completed_filter'] = ''
        else:
            context['completed_filter'] = completed
        return context


@login_required
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


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = UpdateTaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    elif request.method == 'POST':
        try:
            form = UpdateTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError as e:
            error_message = str(e)
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': error_message})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        if task.completed:
            task.completed_at = timezone.now()
        else:
            task.completed_at = None
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.delete()
    return redirect('tasks')


@login_required
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
