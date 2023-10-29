from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class aboutTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.access_names = {
            reverse('about:author'):
                'about/author.html',
            reverse('about:tech'):
                'about/tech.html'
        }

    def test_access(self):
        for url in self.access_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template(self):
        for url, template in self.access_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
