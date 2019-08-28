from django.urls import resolve
from django.test import TestCase

from .views import home_page
from .models import Machine, Breakdown
from .forms import BreakdownForm


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_view_renders_home_page_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_breakdown_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], BreakdownForm)

    def test_home_page_can_save_breakdown_from_POST_request(self):
        machine = Machine.objects.create(name='Machine 1')
        start_time = '2009-10-25 14:30'
        end_time = '2009-10-25 15:30'
        data = {'machine': machine.id, 'start_time': start_time,
                'end_time': end_time}
        self.client.post(
            '/', data=data
        )

        self.assertEqual(Breakdown.objects.all().count(), 1)
