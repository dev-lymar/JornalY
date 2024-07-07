from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'text': 'Это главная страница проекта JornalY'
    }
    template = 'posts/index.html'
    return render(request, template, context=context)


def group_posts(request, slug):
    context = {
        'text': 'Здесь будет информация о группах проекта JornalY'
    }
    template = 'posts/group_list.html'
    return render(request, template, context=context)

