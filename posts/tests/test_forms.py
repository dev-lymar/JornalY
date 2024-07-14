import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

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
        small_img = (
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.jpeg',
            content=small_img,
            content_type='image/jpeg'
        )
        form_data = {
            'pk': 101,
            'text': 'Edited text',
            'group': 100,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'pk': self.post.pk}),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': 'testuser'}))

        edited_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(edited_post.text, 'Edited text')