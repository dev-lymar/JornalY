from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница')


def group_posts(request):
    return HttpResponse('Посты')


def group_detail(request, slug):
    return HttpResponse(f'Пост - {slug}')
