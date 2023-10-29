"""View-функции приложения Posts"""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Group, Post, User


@login_required
def index(request):
    """Выводим содержимое главной страницы"""

    template = 'posts/index.html'

    title = 'Последние обновления на сайте'
    text = 'Это главная страница проекта Yatube'

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'title': title,
               'text': text,
               'page_obj': page_obj}

    return render(request, template, context)


def group_posts(request, slug):
    """Выводим содержимое страницы сообщества (группы)"""

    template = 'posts/group_list.html'

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    title = group.title
    description = group.description

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'group': group,
               'posts': posts,
               'title': title,
               'description': description,
               'page_obj': page_obj}

    return render(request, template, context)


def profile(request, username):

    template = 'posts/profile.html'

    user = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=user).count()
    all_posts = Post.objects.filter(author=user)[:5]

    context = {
        'user': user,
        'post_count': post_count,
        'all_posts': all_posts
    }

    return render(request, template, context)


def post_detail(request, post_id):

    template = 'posts/post_detail.html'

    post = get_object_or_404(Post, pk=post_id)
    user = post.author
    post_count = Post.objects.filter(author=user).count()

    context = {
        'post': post,
        'post_count': post_count
    }

    return render(request, template, context)
