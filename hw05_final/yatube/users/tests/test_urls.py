from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import CreationForm

User = get_user_model()


class UsersURLTests(TestCase):
    """ тесты модуля urls приложения users """

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.user = User.objects.create_user(username='HasNoName2')
        self.authorized_client.force_login(self.user)

        email = {
            'uidb64': 'Ts',
            'token': 'q1w2e3r4'
        }

        self.access_guest_names = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:password_reset'): 'users/password_reset_form.html',
            reverse('users:password_reset_done'):
                'users/password_reset_done.html',
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': email['uidb64'], 'token': email['token']}
            ):
                'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'):
                'users/password_reset_complete.html'
        }

        self.access_authorised_names = {
            reverse('users:password_change'):
                'users/password_change_form.html',
            reverse('users:password_change_done'):
                'users/password_change_done.html',
        }

    def test_guests_access(self):
        """ цикл проверки страниц общего доступа """

        for url in self.access_guest_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_auth_access(self):
        """ цикл проверки страниц для авторизованных пользователей """

        for url in self.access_authorised_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template_guest(self):
        """ цикл проверки соответствия шаблонов страниц общего доступа """

        for url, template in self.access_guest_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_template_auth(self):
        """ проверка соответствия шаблонов:
        (1) выход из учётной записи
        (2) форма смены пароля
        (3) уведомление о смене пароля
        """
        response = self.authorized_client.get('/auth/logout/')
        self.assertTemplateUsed(response, 'users/logged_out.html')
        response = self.authorized_client.get('/auth/password_change/')

        self.assertRedirects(
            response,
            '/auth/login/?next=/auth/password_change/'
        )

        response = self.authorized_client.get('/auth/password_change/done/')

        self.assertRedirects(
            response,
            '/auth/login/?next=/auth/password_change/done/'
        )

    def test_context_signup(self):
        """ проверка контекста страницы регистрации """
        response = self.guest_client.get(reverse('users:signup'))
        result = response.context.get('form')
        self.assertIsInstance(result, CreationForm)


class UserCreateTest(TestCase):
    """ тест создания нового пользователя """

    def setUp(self):
        self.guest = Client()

    def test_create_new_user(self):
        """ проверка создания нового пользователя:
        (1) редирект на главную после создания
        (2) проверка существования нового пользователя
        (3) проверка количества пользователей
        """
        user_count = User.objects.count()

        form_data_user = {
            'first_name': 'Vasya',
            'last_name': 'Popov',
            'username': 'vasyaaa',
            'email': 'email@email.ru',
            'password1': 'qawsedrf1234',
            'password2': 'qawsedrf1234',
        }

        response = self.guest.post(
            reverse('users:signup'),
            data=form_data_user,
            follow=True,
        )

        self.assertRedirects(response, reverse('posts:index'))

        self.assertTrue(
            User.objects.filter(
                first_name='Vasya',
                last_name='Popov',
                username='vasyaaa',
            )
            .exists()
        )
        self.assertEqual(User.objects.count(), user_count + 1)
