from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import PostForm, CommentForm
from .models import Post, Group, Comment


User = get_user_model()


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post List'
        return context


class ProfileView(ListView):
    model = Post
    template_name = 'posts/profile.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.user).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['count_author_posts'] = self.get_queryset().count
        return context


class PostCreateView(CreateView):
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


class PostEditView(UpdateView):
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


class AddCommentView(FormView):
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
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        self.group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return Post.objects.filter(group=self.group).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Community posts by {self.group.title}.'
        context['group'] = self.group
        return context
