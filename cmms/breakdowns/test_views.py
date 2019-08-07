from django.urls import resolve
from django.test import TestCase

from .views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_view_renders_home_page_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
