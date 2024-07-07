from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Group


def index(request):
    keyword = request.GET.get('q', None)
    if keyword:
        posts = Post.objects.filter(text__contains=keyword).select_related('author').select_related('group')
    else:
        posts = None
    context = {
        'title': 'Search by post',
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

