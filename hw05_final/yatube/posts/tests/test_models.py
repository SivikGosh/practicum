from django.test import TestCase

from ..models import Group, Post, User


class PostsModelsTests(TestCase):
    """ тесты модуля models приложения рosts """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(
            username='Test User',
            password='1029384756'
        )

        cls.group = Group.objects.create(
            description='Тестовое описание',
            title='Тестовый заголовок',
            slug='test-slug'
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date='13.08.1990',
            author=PostsModelsTests.user,
            group=PostsModelsTests.group
        )

    def setUp(self):
        self.group = PostsModelsTests.group
        self.post = PostsModelsTests.post

    def test_models_have_correct_object_names(self):
        """ цикл проверки метода __str__ """

        str_names = {
            self.group.__str__(): self.group.title,
            self.post.__str__(): self.post.text[:15]
        }

        for key, value in str_names.items():
            with self.subTest(key=key):
                self.assertEqual(key, value)

    def test_verbose_name(self):
        """ проверка verbose_name:
        (1) модели поста
        (2) модели группы
        """
        post = PostsModelsTests.post

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

        group = PostsModelsTests.group

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
        """ help_text в полях совпадает с ожидаемым:
        (1) для модели поста
        (2) для модели группы
        """
        post = PostsModelsTests.post

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

        group = PostsModelsTests.group

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
