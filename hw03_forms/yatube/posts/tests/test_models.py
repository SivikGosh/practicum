from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост'
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        group_str = group.__str__()
        self.assertEqual(group_str, PostModelTest.group.title)

        post = PostModelTest.post
        post_str = post.__str__()
        self.assertEqual(post_str, PostModelTest.post.text[:15])

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        post_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Сообщество'
        }
        for field, value in post_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    value
                )

        group = PostModelTest.group
        group_verboses = {
            'description': 'Описание',
            'title': 'Имя',
            'slug': 'Адрес',
        }
        for field, value in group_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    value
                )

    def test_help_text(self):
        """help_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        post_helps = {
            'text': 'Текст нового поста',
            'pub_date': 'Дата публикации поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for field, value in post_helps.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text,
                    value
                )

        group = PostModelTest.group
        group_helps = {
            'description': 'Описание группы',
            'title': 'Название группы',
            'slug': 'Адрес группы в адресной строке',
        }
        for field, value in group_helps.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text,
                    value
                )
