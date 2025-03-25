from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Password
from .forms import UserRegistrationForm, PasswordForm
from .views import generate_random_password
import string


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_password_creation(self):
        password = Password.objects.create(
            site='example.com',
            username='testuser',
            password='secure123',
            user=self.user
        )
        self.assertEqual(password.site, 'example.com')
        self.assertEqual(password.user.username, 'testuser')
        self.assertEqual(str(password), 'example.com')


class FormTests(TestCase):
    def test_user_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'user@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_form_valid(self):
        user = User.objects.create_user('formuser', 'user@example.com', 'testpass123')
        form_data = {
            'site': 'example.com',
            'username': 'formuser',
            'password': 'testpass'
        }
        form = PasswordForm(data=form_data, user=user)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.password = Password.objects.create(
            site='example.com',
            username='testuser',
            password='secure123',
            user=self.user
        )

    def test_password_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('password_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'example.com')

    def test_password_add_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('password_add'), {
            'site': 'new.com',
            'username': 'newuser',
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Password.objects.filter(site='new.com').exists())

    def test_generate_random_password_function(self):
        password = generate_random_password()
        self.assertEqual(len(password), 12)
        self.assertTrue(any(c in string.ascii_letters for c in password))
        self.assertTrue(any(c in string.digits for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_password_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('password_delete', args=[self.password.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Password.objects.filter(id=self.password.id).exists())


class AuthTests(TestCase):
    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        User.objects.create_user('loginuser', 'user@example.com', 'testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)