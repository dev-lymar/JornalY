from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.group = Group.objects.create(title='Test Group', slug='test-group', description='Test description')
        cls.post = Post.objects.create(
            id=100,
            text='Test text',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_page(self):
        response = self.guest_client.get('/group/test-slug')
        self.assertEqual(response.status_code, 301)

    def test_user_profile_page(self):
        response = self.guest_client.get('/profile/testuser')
        self.assertEqual(response.status_code, 301)

    def test_post_page(self):
        response = self.guest_client.get('/posts/100/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_page_only_for_author(self):
        response = self.authorized_client.get('/posts/100/edit/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_only_for_authorized_user(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)
