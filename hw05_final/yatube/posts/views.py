""" view-функции приложения posts """

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .serializers import GroupSerializer, PostSerializer
from .utils import posts_paginator

POST_AMOUNT = 10


@cache_page(20, key_prefix='index_page')
def index(request):
    """ выводим содержимое главной страницы """
    template = 'posts/index.html'
    posts = Post.objects.select_related('author').select_related('group').all()
    page_obj = posts_paginator(request, posts, POST_AMOUNT)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def group_posts(request, slug):
    """ выводим содержимое страницы группы """
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author').all()
    page_obj = posts_paginator(request, posts, POST_AMOUNT)
    context = {'group': group, 'page_obj': page_obj}
    return render(request, template, context)


def profile(request, username):
    """ выводим содержимое страницы профиля пользователя """
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=author).count()
    all_posts = Post.objects.select_related('group').filter(author=author)
    page_obj = posts_paginator(request, all_posts, POST_AMOUNT)
    following = False

    if request.user.is_authenticated:
        following = (
            Follow.objects.filter(user=request.user, author=author).exists()
        )

    context = {
        'author': author,
        'post_count': post_count,
        'page_obj': page_obj,
        'following': following
    }

    return render(request, template, context)


def post_detail(request, post_id):

    template = 'posts/post_detail.html'

    post = get_object_or_404(Post, pk=post_id)
    user = post.author
    post_count = user.posts.count()
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post)

    context = {
        'post': post,
        'post_count': post_count,
        'form': form,
        'comments': comments
    }

    return render(request, template, context)


@login_required
def post_create(request):
    """ страница создания поста """

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
    """ страница редактирования поста """
    post = get_object_or_404(Post, pk=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )

    template = 'posts/create_post.html'
    is_edit = True

    if request.user != post.author:
        return redirect('posts:post_detail', post.id)
    elif request.method == 'POST' and form.is_valid:
        post = form.save()
        return redirect('posts:post_detail', post.id)

    context = {'form': form, 'is_edit': is_edit}
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    """ страница добавления комментария """
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """ страница подписаться на автора """
    template = 'posts/follow.html'

    posts = (
        Post.objects.select_related()
        .filter(author__following__user=request.user)
    )

    page_obj = posts_paginator(request, posts, POST_AMOUNT)
    context = {'page_obj': page_obj}
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """ кнопка подписаться на автора """
    author = get_object_or_404(User, username=username)

    try:
        if request.user != author:
            Follow.objects.get_or_create(user=request.user, author=author)
    except IntegrityError:
        return redirect('posts:profile', username=author)

    return redirect('posts:profile', username=author)


@login_required
def profile_unfollow(request, username):
    """ кнопка отписаться от автора """
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=author)


def get_post(request, post_id):
    """получение JSON-объекта поста"""
    if request.method == 'GET':
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    else:
        return None


@api_view(['GET', 'POST'])
def api_posts(request):
    """Работа с постами."""
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_post_detail(request, post_id):
    """Детальная работа с постами."""
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PostSerializer(post)
    return Response(serializer.data)


class APIPost(APIView):
    """Классы API постов."""
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class APIPostDetail(APIView):
    """Классы детали API."""
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIPostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """docstring не придумал пока"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """вьюсет API групп"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
