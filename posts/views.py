from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context=context)


def group_posts(request, slug):
    context = {
        'text': 'Здесь будет информация о группах проекта JornalY'
    }
    return render(request, 'posts/group_list.html', context=context)

