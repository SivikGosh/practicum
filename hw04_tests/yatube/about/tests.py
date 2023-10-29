from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutTests(TestCase):
    """Тесты приложения about"""

    def setUp(self):
        self.client = Client()
        self.access_and_templates = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html'
        }

    def test_access_and_templates(self):
        """

        (1) проверка доступности страницы
        (2) проверка соответствия шаблона

        """
        for url, template in self.access_and_templates.items():
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)
