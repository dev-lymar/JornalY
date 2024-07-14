from django.urls import path

from .views import (AddCommentView, FollowIndexView, GroupPostsView, IndexView,
                    PostCreateView, PostDetailView, PostEditView,
                    ProfileFollowView, ProfileUnfollowView, ProfileView)

app_name = 'posts'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('follow/', FollowIndexView.as_view(), name='follow_index'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/follow/', ProfileFollowView.as_view(), name='profile_follow'),
    path('profile/<str:username>/unfollow/', ProfileUnfollowView.as_view(), name='profile_unfollow'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('group/<slug:slug>/', GroupPostsView.as_view(), name='group_list'),
]
