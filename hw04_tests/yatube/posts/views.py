"""View-функции приложения Posts"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import posts_paginator

POST_AMOUNT = 10


def index(request):
    """Выводим содержимое главной страницы"""

    template = 'posts/index.html'

    posts = Post.objects.select_related().all()

    page_obj = posts_paginator(request, posts, POST_AMOUNT)

    context = {'page_obj': page_obj}

    return render(request, template, context)


def group_posts(request, slug):
    """Выводим содержимое страницы сообщества (группы)"""

    template = 'posts/group_list.html'

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author').all()
    page_obj = posts_paginator(request, posts, POST_AMOUNT)

    context = {'group': group,
               'page_obj': page_obj}

    return render(request, template, context)


def profile(request, username):

    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=author).count()
    all_posts = Post.objects.select_related('group').filter(author=author)
    page_obj = posts_paginator(request, all_posts, POST_AMOUNT)

    context = {
        'author': author,
        'post_count': post_count,
        'page_obj': page_obj
    }

    return render(request, template, context)


def post_detail(request, post_id):

    template = 'posts/post_detail.html'

    post = get_object_or_404(Post, pk=post_id)
    user = post.author
    post_count = user.posts.count()

    context = {
        'post': post,
        'post_count': post_count,
    }

    return render(request, template, context)


@login_required
def post_create(request):

    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('posts:profile', post.author)

    template = 'posts/create_post.html'

    form = PostForm(request.POST or None, files=request.FILES or None)

    context = {'form': form}

    return render(request, template, context)


@login_required
def post_edit(request, post_id):

    post = get_object_or_404(Post, pk=post_id)

    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)

    template = 'posts/create_post.html'
    is_edit = True

    if request.user != post.author:
        return redirect('posts:post_detail', post.id)
    elif request.method == 'POST' and form.is_valid:
        post = form.save()
        return redirect('posts:post_detail', post.id)

    context = {
        'form': form,
        'is_edit': is_edit
    }

    return render(request, template, context)
