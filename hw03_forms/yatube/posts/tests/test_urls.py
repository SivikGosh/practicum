from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date='Тестовая дата',
            author=User.objects.create_user(username='HasNoName'),
        )
        cls.group = Group.objects.create(
            description='Описание',
            title='Имя',
            slug='address'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_author = Client()
        self.user = User.objects.create_user(username='HasNoName2')
        self.authorized_client.force_login(self.user)
        self.authorized_author.force_login(PostURLTests.post.author)

        self.group = PostURLTests.group
        self.post = PostURLTests.post
        self.access_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.post.author.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
        }

    def test_access(self):
        for url in self.access_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        post_id = self.post.pk
        response = self.authorized_author.get(f'/posts/{post_id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_template(self):
        for url, template in self.access_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

        post_id = self.post.pk
        response = self.authorized_author.get(f'/posts/{post_id}/edit/')
        self.assertTemplateUsed(response, 'posts/create_post.html')
