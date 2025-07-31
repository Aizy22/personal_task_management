from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TaskForm
from .models import Task
from django.shortcuts import get_object_or_404
from django.utils import timezone
from collections import defaultdict


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        now = timezone.now()
        today = timezone.localdate()
        
        tasks = Task.objects.filter(user=request.user)
        due_today = tasks.filter(due_date=today, status__in=['not_started', 'in_progress'])
        overdue = [task for task in tasks if task.is_overdue()]
        upcoming = tasks.filter(due_date__gt=today).order_by('due_date')

        # Group by context_tag
        context_grouped_tasks = defaultdict(list)
        for task in due_today:
            context_grouped_tasks[task.get_context_tag_display()].append(task)

        return render(request, 'home.html', {
            'due_today': due_today,
            'overdue': overdue,
            'upcoming': upcoming,
            'context_grouped_tasks': dict(context_grouped_tasks)
        })
    return render(request,'home.html')

#Register
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        
        user = User.objects.create_user(username=username,password=password)
        user.save()
        messages.success(request, 'User registered successfully.')
        return redirect('login')
    
    return render(request, 'register.html')

#Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
        
    return render(request, 'login.html')

#Logout
def logout_user(request):
    logout(request)
    return redirect('login')

#Task CRUD operations
def task_list(request):
    status_filter = request.GET.get('status')  # Getting status =value from url
    if status_filter:
        tasks = Task.objects.filter(user=request.user, status=status_filter)
    else:
        tasks = Task.objects.filter(user=request.user)

    context_tag = request.GET.get('context_tag')
    if context_tag:
        tasks = tasks.filter(context_tag=context_tag)

    return render(request, 'task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request,'task_form.html',{'form':form})

def task_edit(request,pk):
    task = get_object_or_404(Task,pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance =task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance = task)
    return render(request, 'task_form.html',{'form':form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html',{'task': task})
