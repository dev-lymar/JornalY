from django.urls import path
from .views import index, profile, post_detail, group_posts, PostCreateView, PostEditView

app_name = 'posts'

urlpatterns = [
    path('', index, name='home'),
    path('profile/<str:username>/', profile, name='profile'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('group/<slug:slug>/', group_posts, name='group_list'),
]
