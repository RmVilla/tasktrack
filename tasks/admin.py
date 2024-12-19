from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'due_date', 'is_completed')
    search_fields = ('title', 'user__username')
    list_filter = ('is_completed', 'due_date')
