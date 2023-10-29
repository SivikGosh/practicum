from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostsURLTests(TestCase):
    """ тесты модуля urls приложения posts """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(
            username='User Name',
            password='1029384756'
        )

        cls.author = User.objects.create_user(
            username='Author Name',
            password='0192837465'
        )

        cls.group = Group.objects.create(
            description='Тестовое описание',
            title='Тестовое название',
            slug='test-slug'
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date='13.08.1990',
            author=PostsURLTests.author
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorised_client = Client()
        self.authorized_author = Client()
        self.authorised_client.force_login(PostsURLTests.user)
        self.authorized_author.force_login(PostsURLTests.author)
        self.user = PostsURLTests.user
        self.group = PostsURLTests.group
        self.post = PostsURLTests.post

        self.public_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}):
                'posts/post_detail.html'
        }

        self.private_names = {
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}):
                'posts/create_post.html'
        }

        cache.clear()

    def test_httpstatus(self):
        """ проверка доступности страницы:
        (1),(2) циклы проверкок общедоступных страниц
        (3),(4) проверка страниц авторизованными пользователями
        (5) возврат 404 на несуществующую страницу
        """

        for url, _ in self.public_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

        for url, _ in self.private_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.authorised_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.authorised_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_templates(self):
        """ проверка доступности шаблонов:
        (1) цикл проверки общедоступных страниц
        (2) цикл проверки страниц для авторизованных пользователей
        (3) возврат шаблона несуществующей страницы
        """

        for url, template in self.public_names.items():
            with self.subTest(url=url):
                response = self.authorized_author.get(url)
                self.assertTemplateUsed(response, template)

        for url, template in self.private_names.items():
            with self.subTest(url=url):
                response = self.authorized_author.get(url)
                self.assertTemplateUsed(response, template)

        response = self.guest_client.get('/unexisting_page/')
        self.assertTemplateUsed(response, 'core/404.html')
