from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, Comment

User = get_user_model()


class PostViewsTests(TestCase):
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

    def test_pages_uses_correct_template(self):
        """The URL uses the appropriate template."""
        templates_pages_names = {
            'posts/index.html': reverse('posts:home'),
            'posts/group_list.html': reverse('posts:group_list', kwargs={'slug': 'test-group'}),
            'posts/profile.html': reverse('posts:profile', kwargs={'username': 'testuser'}),
            'posts/post_detail.html': reverse('posts:post_detail', kwargs={'post_id': 100}),
            'posts/create_post.html': reverse('posts:post_edit', kwargs={'pk': 100}),
            'posts/create_post.html': reverse('posts:post_create'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """The home template is formed with the correct context."""
        """The home template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:home'))
        self.assertEqual(response.context['title'], 'Search by post')

    def test_pagination(self):
        """The home page paginates posts correctly."""
        posts = [
            Post(text=f'Test text {i}', author=self.user, group=self.group)
            for i in range(14)
        ]
        Post.objects.bulk_create(posts)

        response = self.authorized_client.get(reverse('posts:home'))
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.authorized_client.get(reverse('posts:home') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_authorized_user_can_comment(self):
        """Ensure that an authenticated user can comment on a post."""
        comment_count_before = Comment.objects.count()
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data={'text': 'Test comment'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), comment_count_before + 1)
        self.assertTrue(Comment.objects.filter(text="Test comment").exists())

    def test_comment_appears_on_post_page(self):
        """Ensure that after commenting, the comment appears on the post detail page."""
        comment_text = 'Another test comment'
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data={'text': comment_text},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment_text)
