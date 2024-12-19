from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def task_list(request):
    tasks = Task.objects.all()
    filter_status = request.GET.get('status')

    if filter_status:
        tasks = tasks.filter(is_completed=(filter_status == 'completed'))

    return render(request, 'tasktrack/task_list.html', {'tasks': tasks})


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasktrack/task_detail.html', {'task': task})


@login_required
def create_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            user=request.user
        )
        return redirect('task_list')
    return render(request, 'tasktrack/create_task.html')


@login_required
def mark_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True
    task.save()
    return redirect('task_list')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

