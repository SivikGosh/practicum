import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Page
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post, User
from posts.views import POST_AMOUNT

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTests(TestCase):
    """Тесты модуля views приложения Posts"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        posts_amount = 11

        img = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
               b'\x01\x00\x80\x00\x00\x00\x00\x00'
               b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
               b'\x00\x00\x00\x2C\x00\x00\x00\x00'
               b'\x02\x00\x01\x00\x00\x02\x02\x0C'
               b'\x0A\x00\x3B')

        uploaded = SimpleUploadedFile(name='image.gif',
                                      content=img,
                                      content_type='image/gif')

        cls.user = User.objects.create_user(username='Test User',
                                            password='1029384756')

        cls.group = Group.objects.create(description='Тестовое описание',
                                         title='Тестовый заголовок',
                                         slug='test-slug')

        cls.second_group = Group.objects.create(description='Второе описание',
                                                title='Второй заголовок',
                                                slug='second-test-slug')

        cls.posts_list = [Post(text='Тестовый текст',
                               pub_date='13.08.1990',
                               author=PostsViewsTests.user,
                               group=PostsViewsTests.group,
                               image=uploaded)
                          for post in range(posts_amount)]

        Post.objects.bulk_create(cls.posts_list)
        cls.posts = Post.objects.all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorised_client = Client()
        self.authorised_client.force_login(PostsViewsTests.user)

        self.group = PostsViewsTests.group
        self.user = PostsViewsTests.user
        self.post = PostsViewsTests.posts[0]

    def loop_method_context(self, context, response):
        """цикл проверки контекста, передаваемых в шаблон"""

        for key, value in context.items():
            with self.subTest(key=key):
                result = response.context.get(key)
                self.assertIsInstance(result, value)

    def test_paginator(self):
        """проверка паджинатора:

        (1) кол-во постов на первой странице
        (2) кол-во постов на второй странице

        """
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), POST_AMOUNT)

        post_second_page = 1
        response = self.guest_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']),
                         post_second_page)

    def test_templates(self):
        """проверка доступности шаблонов"""
        templates = {
            reverse('posts:index'):
                'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}):
                'posts/post_detail.html',
            reverse('posts:post_create'):
                'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}):
                'posts/create_post.html'}

        for url, template in templates.items():
            with self.subTest(url=url):
                response = self.authorised_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_index_page_context(self):
        """проверка типа контекста главной страницы:

        (1) page_obj
        (2) картинка у поста
        (3) паджинатор

        """
        response = self.guest_client.get(reverse('posts:index'))

        result = response.context.get('page_obj')
        result_image = response.context.get('page_obj')[0].image

        # Тесты #

        self.assertIsInstance(result, Page)
        self.assertIsInstance(result_image, type(self.post.image))
        self.test_paginator()

    def test_group_list_page_context(self):
        """проверка типа контекста страницы постов группы

        (1) цикл проверки группы и page_obj
        (2) картинка у поста
        (3) паджинатор

        """
        response = self.guest_client.get(reverse('posts:group_list',
                                         kwargs={'slug': self.group.slug}))

        context = {'group': Group, 'page_obj': Page}

        result_image = response.context.get('page_obj')[0].image

        # Тесты #

        self.loop_method_context(context, response)
        self.assertIsInstance(result_image, type(self.post.image))
        self.test_paginator()

    def test_profile_context(self):
        """проверка типа контекста страницы профиля пользователя:

        (1) цикл проверки автора, счётчика постов, page_obj
        (2) картинка у поста
        (3) паджинатор

        """
        response = self.guest_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}))

        context = {'author': User,
                   'post_count': int,
                   'page_obj': Page}

        result_image = response.context.get('page_obj')[0].image

        # Тесты #

        self.loop_method_context(context, response)
        self.assertIsInstance(result_image, type(self.post.image))
        self.test_paginator()

    def test_post_detail_context(self):
        """проверка типа контекста детальной страницы поста

        (1) цикл проверки поста и счётчика постов
        (2) картинка у поста

        """
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}))

        context = {'post': Post, 'post_count': int}

        result_image = response.context.get('post').image

        # Тесты #

        self.loop_method_context(context, response)
        self.assertIsInstance(result_image, type(self.post.image))

    def test_create_post_context(self):
        """проверка типа контекста страницы создания поста"""
        response = self.authorised_client.get(reverse('posts:post_create'))
        result = response.context.get('form')
        self.assertIsInstance(result, PostForm)

    def test_edit_post_context(self):
        """проверка типа контекста страницы редактирования поста"""
        response = self.authorised_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}))

        context = {'form': PostForm, 'is_edit': bool}

        self.loop_method_context(context, response)

    def test_contains_post(self):
        """проверка появления поста после его создания:

        (1) на главной странице
        (2) на странице группы, к которой относится пост
        (3) на странице автора поста
        (4) отсутствие поста на странице, к которой он не относится

        """
        response_index = self.guest_client.get(reverse('posts:index'))

        response_group_list = self.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))

        response_profile = self.guest_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}))

        response_second_group = self.guest_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': PostsViewsTests.second_group.slug}))

        # Тесты #

        self.assertContains(response_index, self.post)
        self.assertContains(response_group_list, self.post)
        self.assertContains(response_profile, self.post)
        self.assertNotContains(response_second_group, self.post)
