from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

class UserAuthenticationTest(TestCase):
    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login(self):
        user = User.objects.create_user(username='testuser', password='password123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_logout(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout


