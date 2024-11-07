from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Task
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
@login_required
def home(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {
        'tasks': tasks,
    })

@login_required
def completed(request):
    completed_tasks = Task.objects.filter(completed=True)

    return render(request, 'completed.html', {
        'tasks': completed_tasks,
    })

@login_required
def remaining(request):
    remaining_tasks = Task.objects.filter(completed=False)
    return render(request, 'remaining.html', {
        'tasks': remaining_tasks,
    })

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        due_time = request.POST.get('due_time')
        assigned_email = request.POST.get('assigned_email')
        completed = False

        if title != "" and due_date != "" and due_time !="":
            task = Task(
                title=title,
                description=description,
                due_date=due_date,
                due_time=due_time,
                completed=completed,
                assigned_email=assigned_email
            )
            task.save()
            if assigned_email:
                send_mail(
                    subject=f"New Task Assigned: {title}",
                    message=f"Task Description: {description}\nDue Date: {due_date} at {due_time}",
                    from_email="denaro2012@gmail.com",
                    recipient_list=[assigned_email],
                    fail_silently=False,
                )
            
            return redirect('home')
    else:
        return render(request, 'add_task.html') 
    return render(request, 'add_task.html')

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'delete.html', {
        "task": task,
    })

@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'task_detail.html', {
        "task": task,
    })

@login_required
def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    if task:
        task.completed = not task.completed
        task.save()
        return redirect('home')

@login_required
def remove_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        messages.success(request, "Task successfully deleted.")
    except Task.DoesNotExist:
        messages.error(request, "Task not found.")
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')  # Redirect to the main page after sign-up
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirect to your main page after login
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})