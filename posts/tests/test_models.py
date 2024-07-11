from django.contrib.auth.models import User
from django.test import TestCase
from posts.models import Post, Group


class BaseModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.group = Group.objects.create(title='Test Group', description='Test description')


class PostModelTest(BaseModelTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Test text',
            author=cls.user,
            group=cls.group
        )

    def test_model_have_correct_object_names(self):
        self.assertEqual(str(self.post), 'Test text')


class GroupModelTest(BaseModelTest):
    def test_model_have_correct_object_names(self):
        self.assertEqual(str(self.group), 'Test Group')