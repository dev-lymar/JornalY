from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

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
        """Checking if the homepage is available."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_page(self):
        """"Check the availability of the group page and redirect to the correct URL."""
        response = self.guest_client.get(reverse('posts:group_list', kwargs={'slug': 'test-group'}))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_page(self):
        """Check if the user profile page is available and redirect to the correct URL."""
        response = self.guest_client.get(reverse('posts:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        """Checking if the post page is available."""
        response = self.guest_client.get(reverse('posts:post_detail', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 200)

    def test_post_edit_page_only_for_author(self):
        """Check if the post edit page is available for the author only."""
        response = self.authorized_client.get(reverse('posts:post_edit', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 200)

    def test_post_create_only_for_authorized_user(self):
        """"Check if the post creation page is only available to an authorised user."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 200)
