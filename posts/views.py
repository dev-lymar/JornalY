from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import PostForm, CommentForm
from .models import Post, Group, Comment

User = get_user_model()


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    keyword = request.GET.get('q', None)
    if keyword:
        posts = Post.objects.filter(text__contains=keyword).select_related('author').select_related('group')
    else:
        posts = None
    context = {
        'title': 'Search by post',
        'page_obj': page_obj,
        'posts': posts,
    }
    return render(request, 'posts/index.html', context=context)


def profile(request, username):
    user = get_object_or_404(User, username=username)

    post_list = Post.objects.all().filter(author=user).order_by('-pub_date')
    count_author_posts = post_list.count()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'user': user,
        'page_obj': page_obj,
        'count_author_posts': count_author_posts,
    }
    return render(request, 'posts/profile.html', context=context)


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


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    count_author_posts = Post.objects.filter(author=post.author).count()
    comments = Comment.objects.filter(post=post).order_by('-created')
    form = CommentForm()

    context = {
        'post': post,
        'count_author_posts': count_author_posts,
        'comments': comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context=context)


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post, 'form': form})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'title': f'Community posts by {group.title}.',
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context=context)
