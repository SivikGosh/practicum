"""URL-адреса в приложении Posts"""

from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('index.html', views.index, name='index'),
    path('', views.index, name='index'),
    path('group/<slug>/', views.group_posts, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail')
]
