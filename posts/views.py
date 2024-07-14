from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import PostForm, CommentForm
from .models import Post, Group, Comment, Follow
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.models import AnonymousUser


User = get_user_model()


@method_decorator(cache_page(60), name='get')
class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post List'
        return context


class FollowIndexView(ListView, LoginRequiredMixin):
    model = Follow
    template_name = 'posts/follow.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author__following__user=self.request.user).order_by('-pub_date')


class ProfileFollowView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        username = self.kwargs.get('username')
        user_to_follow = get_object_or_404(User, username=username)
        if user_to_follow != self.request.user:
            Follow.objects.get_or_create(user=self.request.user, author=user_to_follow)
        return reverse_lazy('posts:profile', kwargs={'username': username})


class ProfileUnfollowView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        username = self.kwargs.get('username')
        user_to_unfollow = get_object_or_404(User, username=username)
        Follow.objects.filter(user=self.request.user, author=user_to_unfollow).delete()
        return reverse_lazy('posts:profile', kwargs={'username': username})


class ProfileView(ListView):
    model = Post
    template_name = 'posts/profile.html'
    paginate_by = 10
    context_object_name = 'page_obj'

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.author).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['author'] = self.author
        context['count_author_posts'] = self.get_queryset().count()
        if isinstance(user, AnonymousUser):
            context['following'] = False
        else:
            context['following'] = Follow.objects.filter(user=user, author=self.author).exists()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def get_success_url(self):
        return reverse_lazy('posts:profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def get_success_url(self):
        return reverse_lazy('posts:profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('posts:post_detail', post_id=post.pk)
        return super().dispatch(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_author_posts'] = Post.objects.filter(author=self.object.author).count()
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created')
        context['form'] = CommentForm
        return context


class AddCommentView(LoginRequiredMixin, FormView):
    form_class = CommentForm
    template_name = 'posts/post_detail.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        comment.save()
        return redirect('posts:post_detail', pk=post.pk)

    def form_invalid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.render_to_response(self.get_context_data(form=form, post=post))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(post=context['post']).order_by('-created')
        context['count_author_posts'] = Post.objects.filter(author=context['post'].author).count()
        context['form'] = self.get_form()
        return context


class GroupPostsView(ListView):
    model = Post
    template_name = 'posts/group_list.html'
    paginate_by = 10

    def get_queryset(self):
        self.group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return Post.objects.filter(group=self.group).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Community posts by {self.group.title}.'
        context['group'] = self.group
        return context
