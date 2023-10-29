from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import GroupViewSet, PostViewSet

app_name = 'posts'

router = routers.SimpleRouter()
router.register('api/v1/posts', PostViewSet)
router.register('api/v1/group', GroupViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment/',
         views.add_comment, name='add_comment'),
    path('follow/', views.follow_index, name='follow_index'),
    path('profile/<str:username>/follow/',
         views.profile_follow, name='profile_follow'),
    path('profile/<str:username>/unfollow/',
         views.profile_unfollow, name='profile_unfollow'),
    # path('api/v1/posts/<int:post_id>/', views.get_post, name='get_post'),
    path('api/v1/posts/', views.api_posts, name='api_posts'),
    path('api/v1/posts/<int:post_id>/',
         views.api_post_detail, name='api_post_detail'),
    # path('api/v1/posts/', APIPost.as_view(), name='api_posts'),
    # path('api/v1/posts/<int:post_id>/',
    #      APIPostDetail.as_view(), name='api_post_detail'),
    # path('api/v1/posts/', APIPostList.as_view(), name='api_posts'),
    # path('api/v1/posts/<int:pk>/',
    #      APIPostDetail.as_view(), name='api_post_detail'),
    path('', include(router.urls)),
    path('api/v1/api-token-auth/', obtain_auth_token)
]
