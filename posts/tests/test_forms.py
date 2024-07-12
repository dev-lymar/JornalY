from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, Group

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.group = Group.objects.create(id=100, title='Test Group', slug='test-group', description='Test description')
        cls.post = Post.objects.create(
            id=100,
            text='Test text',
            author=cls.user,
            group=cls.group
        )
        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_creating_post_authorized_user(self):
        """A valid form creates a record in Post."""
        posts_count = Post.objects.count()
        form_data = {
            'pk': 101,
            'text': 'Test text',
            'group': 100,
            'author': self.authorized_client
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': 'testuser'}))

        self.assertEqual(Post.objects.count(), posts_count+1)

        self.assertTrue(
            Post.objects.filter(
                text='Test text',
                group=100,
            ).exists()
        )

    def test_edit_post_by_author(self):
        """A valid form edits a post by the author."""
        form_data = {
            'pk': 101,
            'text': 'Edited text',
            'group': 100,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'pk': self.post.pk}),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': 'testuser'}))

        edited_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(edited_post.text, 'Edited text')