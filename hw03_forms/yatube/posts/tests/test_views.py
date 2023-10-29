from django.contrib.auth import get_user_model
from django.core.paginator import Page
from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()


class ViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Имя Фамильевич')
        cls.group = Group.objects.create(
            description='Описание тестовой группы',
            title='Название тестовой группы',
            slug='some-slug'
        )
        cls.fake_group = Group.objects.create(
            description='Описание фейка',
            title='Название фейка',
            slug='fake-slug'
        )
        cls.post = [Post.objects.create(
            text='Текстовый текст',
            pub_date='17.08.2022',
            author=ViewsTests.user,
            group=ViewsTests.group
        )
            for i in range(11)
        ]

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def loop_method_context(self, context, response):
        for key, value in context.items():
            with self.subTest(key=key):
                result = response.context.get(key)
                self.assertIsInstance(result, value)

    def test_first_page_contains_ten_records(self):
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_ten_records(self):
        response = self.guest_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_templates(self):
        templates_for_guests_names = {
            reverse('posts:index'):
                'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'some-slug'}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'Имя Фамильевич'}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': '1'}):
                'posts/post_detail.html',
            reverse('posts:post_create'):
                'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': '1'}):
                'posts/create_post.html'
        }

        for url, template in templates_for_guests_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_index_page_context(self):
        response = self.guest_client.get(reverse('posts:index'))
        result = response.context.get('page_obj')
        self.assertIsInstance(result, Page)
        self.test_first_page_contains_ten_records()
        self.test_second_page_contains_ten_records()

    def test_group_list_page_context(self):
        response = self.guest_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': ViewsTests.group.slug}
            )
        )

        context = {
            'group': Group,
            'page_obj': Page
        }

        self.loop_method_context(context, response)
        self.test_first_page_contains_ten_records()
        self.test_second_page_contains_ten_records()

    def test_profile_context(self):
        response = self.guest_client.get(
            reverse('posts:profile', kwargs={'username': ViewsTests.user})
        )

        context = {
            'author': User,
            'post_count': int,
            'page_obj': Page
        }

        self.loop_method_context(context, response)
        self.test_first_page_contains_ten_records()
        self.test_second_page_contains_ten_records()

    def test_post_detail_context(self):
        post = ViewsTests.post[0]
        response = self.guest_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': post.pk}
            )
        )

        context = {
            'post': Post,
            'post_count': int
        }

        self.loop_method_context(context, response)

    def test_create_post_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        result = response.context.get('form')
        self.assertIsInstance(result, PostForm)

    def test_edit_post_context(self):
        post = ViewsTests.post[0]
        response = self.authorized_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': post.pk}
            )
        )

        context = {
            'form': PostForm,
            'is_edit': bool
        }

        self.loop_method_context(context, response)

    def test_contains_post(self):
        response_index = self.guest_client.get(reverse('posts:index'))
        response_group_list_ = self.guest_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': ViewsTests.group.slug}
            )
        )
        response_profile = self.guest_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': ViewsTests.user.username}
            )
        )
        response_fake_group = self.guest_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': ViewsTests.fake_group.slug}
            )
        )

        post = ViewsTests.post[0]
        self.assertContains(response_index, post)
        self.assertContains(response_group_list_, post)
        self.assertContains(response_profile, post)
        self.assertNotContains(response_fake_group, post)
