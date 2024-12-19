from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

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
        due_date_str = request.POST.get('due_date')  # Get the string from the form input

        try:
            # Parse the date string into a datetime object
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')  # Adjust the format as needed
            due_date = timezone.make_aware(due_date)  # Make it timezone-aware
        except ValueError:
            # Handle invalid date format (e.g., log the error or display a message)
            # This is just an example; you could handle the error more gracefully.
            return render(request, 'tasktrack/create_task.html', {'error': 'Invalid date format'})

        # Create the task with the validated data
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



