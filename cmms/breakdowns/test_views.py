import unittest

from django.urls import resolve
from django.test import TestCase

from .views import home_page
from .models import Machine, Breakdown
from .forms import BreakdownForm

import sys


class HomePageTest(TestCase):
    def prepare_breakdown_data(
            self,
            machine_name='Machine 1',
            start_time='2009-10-25 14:30',
            end_time='2009-10-25 15:30',
            breakdown_description='Test brekdown'):
        self.machine = Machine.objects.create(name=machine_name)
        self.breakdown_data = {
            'machine': self.machine.id,
            'start_time': start_time,
            'end_time': end_time,
            'breakdown_description': breakdown_description}
        return self.breakdown_data

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
        breakdown_data = self.prepare_breakdown_data()
        self.client.post(
            '/', data=breakdown_data
        )

        self.assertEqual(Breakdown.objects.all().count(), 1)

    @unittest.skip
    def test_last_breakdown_is_passed_to_template(self):
        breakdowns = []
        breakdown_data = self.prepare_breakdown_data()
        for x in range(10):
            start_time = '2009-10-25 %s:30' % x
            breakdown_data['start_time'] = start_time
            print(breakdown_data, file=sys.stderr)
            breakdown = Breakdown.objects.create(**breakdown_data)
            breakdowns.append(breakdown)
        last_breakdown = self.prepare_breakdown_data(start_time='2009-10-25 9:30')
        response = self.client.get('/')

        self.assertEqual(response.context['last_breakdowns'][0], last_breakdown)


class AllBreakdownsViewTest(TestCase):
    def test_all_breakdowns_template_used(self):
        response = self.client.get('/all_breakdowns')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_breakdowns.html')
