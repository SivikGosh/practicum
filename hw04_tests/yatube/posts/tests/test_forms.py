import shutil
import tempfile
from datetime import datetime
from http import HTTPStatus

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFormsTests(TestCase):
    """Тесты модуля forms приложения Posts"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        img = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
               b'\x01\x00\x80\x00\x00\x00\x00\x00'
               b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
               b'\x00\x00\x00\x2C\x00\x00\x00\x00'
               b'\x02\x00\x01\x00\x00\x02\x02\x0C'
               b'\x0A\x00\x3B')

        cls.uploaded = SimpleUploadedFile(name='image.gif',
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

        cls.post = Post.objects.create(text='Тестовый текст',
                                       author=PostsFormsTests.user,
                                       group=PostsFormsTests.group)

        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client = Client()
        self.guest = Client()
        self.client.force_login(PostsFormsTests.user)

    def test_create_new_post(self):
        """проверка создания нового поста:

        (1) редирект после добавления
        (2) добавлен +1 пост
        (3),(4) существование нового поста в базе
        (5) доступность страницы
        (6) неавторизованный пользователь не попадает на страницу создания
            поста

        """
        posts_count = Post.objects.count()
        added_post = 1

        form_data = {'text': 'Текст добавляемого поста',
                     'group': PostsFormsTests.group.pk,
                     'image': PostsFormsTests.uploaded}

        response = self.client.post(reverse('posts:post_create'),
                                    data=form_data, follow=True)

        guest_response = self.guest.get(reverse('posts:post_create'))

        #   Тесты   #

        self.assertRedirects(
            response, reverse('posts:profile',
                              kwargs={'username': PostsFormsTests.user}))

        self.assertEqual(Post.objects.count(), (posts_count + added_post))

        self.assertEqual(form_data['text'],
                         Post.objects.latest('pub_date').text)

        self.assertEqual(form_data['group'],
                         Post.objects.latest('pub_date').group.pk)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(guest_response.status_code, HTTPStatus.FOUND)

    def test_edit_post(self):
        """проверка редактрирования поста:

        (1) редирект после редактирования
        (2) количество постов
        (3),(4) существование изменённого поста
        (5) отсутствие старой версии поста

        """
        post_id = PostsFormsTests.post.pk
        posts_count = Post.objects.count()

        form_data_2 = {'text': 'Третий тестовый текст',
                       'pub_date': datetime(2022, 8, 23, 3),
                       'group': PostsFormsTests.second_group.pk}

        response = self.client.post(reverse('posts:post_edit',
                                            kwargs={'post_id': post_id}),
                                    data=form_data_2, follow=True)

        #   Тесты   #

        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     kwargs={'post_id': post_id}))

        self.assertEqual(Post.objects.count(), posts_count)

        self.assertEqual(form_data_2['text'],
                         Post.objects.latest('pub_date').text)

        self.assertEqual(form_data_2['group'],
                         Post.objects.latest('pub_date').group.pk)

        self.assertFalse(
            Post.objects.filter(text='Новый текст',
                                group=PostsFormsTests.group).exists())
