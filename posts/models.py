from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Post text', help_text='Enter the text of the post')
    pub_date = models.DateField('Date of publication', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Author')
    group = models.ForeignKey(
        Group, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Group', help_text='Select a group'
    )
    image = models.ImageField('Image', upload_to='posts', blank=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Comment'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Author')
    text = models.TextField('Comment', help_text='Enter the comment of the post')
    created = models.DateField('Created', auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', verbose_name='user')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='author')

    class Meta:
        unique_together = ('user', 'author')
