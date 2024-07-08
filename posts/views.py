from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, Group


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


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'title': f'Community posts by {group.title}.',
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context=context)

