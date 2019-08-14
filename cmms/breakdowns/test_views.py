from django.urls import resolve
from django.test import TestCase

from .views import home_page
from .models import Machine


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_view_renders_home_page_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_sends_all_machines_to_template(self):
        machine_1 = Machine.objects.create(name="Machine 1")
        machine_2 = Machine.objects.create(name="Machine 2")
        machines_list = [machine_1, machine_2]
        response = self.client.get('/')
        self.assertEqual(len(response.context['all_machines']), len(machines_list))
