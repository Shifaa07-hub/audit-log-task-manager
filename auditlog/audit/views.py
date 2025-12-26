from django.shortcuts import render
from .models import Task, AuditLog
from .forms import TaskForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout

# Create your views here.
@login_required
def home(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'home.html', {'logs': logs})

@login_required
def all_task(request):
    tasks = Task.objects.all()
    return render(request, 'task_manager.html', {'tasks':tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid:
            task = form.save (commit=False)
            task.user = request.user
            task.save()
            AuditLog.objects.create(
                user = request.user,
                task = task,
                task_name = task.task,
                action = 'added'
            )
            return redirect('task')
    else:
        form = TaskForm() 
    return render(request, 'add_task.html', {'form':form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance = task)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                user = request.user,
                task = task,
                task_name = task.task,
                action = 'updated'
            )
            return redirect('task')
    else:
        form = TaskForm(instance=task)
    return render(request, 'add_task.html', {'form':form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == "POST":
        AuditLog.objects.create(
            user = request.user,
            task = task,
            task_name = task.task,
            action = 'deleted'
        )
        task.delete()
        return redirect('task')
    return render(request, 'delete_task.html', {'task':task})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('task')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})

def user_logout(request):
    if request.method == "POST":
        logout(request)
    return render(request, 'registration/log_out.html')

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    AuditLog.objects.create(
        user = request.user,
        task = task,
        task_name = task.task,
        action = 'completed' if task.completed else 'incompleted'
    )
    return redirect('task')

def search(request):
    query = request.GET.get('q', '')
    tasks = Task.objects.none()

    if query:
        tasks = Task.objects.filter(task__icontains = query)

    return render(request, 'task_manager.html', {'query':query, 'tasks':tasks})
