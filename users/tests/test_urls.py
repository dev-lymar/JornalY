from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_login_page(self):
        response = self.guest_client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.guest_client.get('/auth/signup/')
        self.assertEqual(response.status_code, 200)

    def test_password_change_only_for_authorized_user(self):
        response = self.authorized_client.get('/auth/password_change/')
        self.assertEqual(response.status_code, 200)
