from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='New Username',
            password='1029384756'
        )
        cls.group = Group.objects.create(
            description='Новое описание',
            title='Новый заголовок',
            slug='new-slug'
        )
        cls.second_group = Group.objects.create(
            description='вторая группа',
            title='второй тайтл',
            slug='second-slug'
        )
        cls.post = Post.objects.create(
            text='Новый текст',
            pub_date='18.08.22',
            author=PostFormTest.user,
            group=PostFormTest.group
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest = Client()
        self.guest.force_login(PostFormTest.user)

    def test_create_new_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Какой-то второй текст',
            'group': PostFormTest.group.pk
        }
        response = self.guest.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': PostFormTest.user})
        )
        self.assertEqual(Post.objects.count(), (posts_count + 1))
        self.assertTrue(Post.objects.filter(**form_data).exists())

    def test_edit_post(self):
        posts_count = Post.objects.count()
        form_data_2 = {
            'text': 'Какой-то nhtnbq текст',
            'group': PostFormTest.group.pk
        }
        response = self.guest.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostFormTest.post.pk}
            ),
            data=form_data_2,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostFormTest.post.pk}
            )
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(Post.objects.filter(**form_data_2).exists())
        self.assertFalse(
            Post.objects.filter(
                text='Новый текст',
                group=PostFormTest.group
            ).exists()
        )
