from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task
from django.test import TestCase

class TaskViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create a task for testing
        self.task = Task.objects.create(
            title='Test Task 1',
            description='Test description',
            due_date='2024-12-31',
            user=self.user
        )

    def test_task_creation(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('create_task'), {
            'title': 'Test Task',
            'description': 'Test description',
            'due_date': '2024-12-31',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after task creation
        self.assertTrue(Task.objects.filter(title='Test Task').exists())

    def test_task_list_view(self):

        # Create tasks for testing
        task1 = Task.objects.create(title='Test Task 1', description='Test description 1', user=self.user, is_completed=False)
        task2 = Task.objects.create(title='Test Task 2', description='Test description 2', user=self.user, is_completed=True)
        
        # Send a GET request to the task list view
        response = self.client.get(reverse('task_list'))
        
        # Check that the tasks are present in the response
        self.assertContains(response, 'Test Task 1')  # Task should be in the list
        self.assertContains(response, 'Test Task 2')  # Task should be in the list
        
        # Filter tasks by 'completed' status
        response = self.client.get(reverse('task_list') + '?status=completed')
        self.assertContains(response, 'Test Task 2')  # Only the completed task should appear
        self.assertNotContains(response, 'Test Task 1')  # Incompleted task should not appear


    def test_task_detail(self):
        task = Task.objects.create(title='Test Task', description='Test description', user=self.user)
        
        # Send a GET request to the task detail view
        response = self.client.get(reverse('task_detail', args=[task.id]))
        
        # Check that the task details are displayed
        self.assertContains(response, 'Test Task')  # Ensure the task title is in the response
        self.assertContains(response, 'Test description')  # Ensure the task description is in the response


    def test_task_deletion(self):
        task = Task.objects.create(title='Test Task', description='Test description', user=self.user)
        
        # Send a GET request to delete the task
        response = self.client.get(reverse('delete_task', args=[task.id]))  # Sending GET request as per your view
        
        # Check that the task has been deleted
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after deletion
        self.assertFalse(Task.objects.filter(id=task.id).exists())  # Ensure the task is deleted



class TaskFilterTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_filter_completed_tasks(self):
        task = Task.objects.create(title='Test Task', description='Test description', user=self.user, is_completed=True)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('task_list') + '?status=completed')
        self.assertContains(response, 'Test Task')  # Ensure completed task appears in the filtered list

    def test_filter_pending_tasks(self):
        task = Task.objects.create(title='Test Task', description='Test description', user=self.user, is_completed=False)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('task_list') + '?status=pending')
        self.assertContains(response, 'Test Task')  # Ensure pending task appears in the filtered list

