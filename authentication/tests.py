from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        # sementara search_url diarahkan ke login_url agar test tidak error
        self.search_url = self.login_url
        # user untuk login
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

    # -------- REGISTER TESTS --------
    def test_register_success(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        })
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'username': 'wronguser',
            'email': 'wrong@example.com',
            'password': '12345',
            'confirm_password': '54321'
        })
        self.assertRedirects(response, self.register_url)
        self.assertFalse(User.objects.filter(username='wronguser').exists())

    def test_register_duplicate_username(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',  
            'email': 'duplicate@example.com',
            'password': '123456',
            'confirm_password': '123456'
        })
        self.assertRedirects(response, self.register_url)

    # -------- LOGIN TESTS --------
    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertRedirects(response, self.search_url)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertRedirects(response, self.login_url)
        self.assertFalse('_auth_user_id' in self.client.session)

    # -------- LOGOUT TEST --------
    def test_logout(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertFalse('_auth_user_id' in self.client.session)
