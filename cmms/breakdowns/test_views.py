from unittest.mock import patch
from unittest import skip

from django.urls import resolve
from django.test import TestCase
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .views import home_page
from .models import Machine, Breakdown
from .forms import BreakdownForm

import sys


class HomePageTest(TestCase):
    def prepare_breakdown_form_data(
            self,
            machine_name='Machine 1',
            start_time='2009-10-01 14:30',
            end_time='2009-10-01 15:30',
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
        breakdown_data = self.prepare_breakdown_form_data()
        self.client.post(
            '/', data=breakdown_data
        )

        self.assertEqual(Breakdown.objects.all().count(), 1)


class AllBreakdownsViewTest(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(name='Machine 1')

    def prepare_breakdown(
            self,
            start_time='2009-10-01 14:30',
            end_time='2009-10-01 15:30',
            breakdown_description='Test breakdown'):
        start_time = timezone.make_aware(parse_datetime(start_time))
        end_time = timezone.make_aware(parse_datetime(end_time))
        Breakdown.objects.create(
            machine=self.machine,
            start_time=start_time,
            end_time=end_time,
            breakdown_description=breakdown_description)

    def test_all_breakdowns_template_used(self):
        response = self.client.get('/all_breakdowns')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_breakdowns.html')

    def test_last_breakdowns_are_passed_to_all_breakdowns_template(self):
        for x in range(10):
            start_time = '2009-10-01 %s:30' % x
            self.prepare_breakdown(start_time=start_time)
        last_breakdown = Breakdown.objects.all().order_by('-end_time')[0]
        response = self.client.get('/all_breakdowns')

        self.assertEqual(response.context['last_breakdowns'][0], last_breakdown)


class BreakdownDetailViewTest(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(name='Machine 1')

    def prepare_breakdown(
            self,
            start_time='2009-10-01 14:30',
            end_time='2009-10-01 15:30',
            breakdown_description='Test breakdown'):
        start_time = timezone.make_aware(parse_datetime(start_time))
        end_time = timezone.make_aware(parse_datetime(end_time))
        Breakdown.objects.create(
            machine=self.machine,
            start_time=start_time,
            end_time=end_time,
            breakdown_description=breakdown_description)

    def test_breakdown_details_template_used(self):
        self.prepare_breakdown()
        breakdown = Breakdown.objects.all()[0]
        breakdown_id = breakdown.pk

        response = self.client.get('/all_breakdowns/details/%s' % breakdown_id)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'breakdown_details.html')

    def test_breakdown_is_passed_to_details_template(self):
        self.prepare_breakdown()
        breakdown = Breakdown.objects.all()[0]
        breakdown_id = breakdown.pk

        response = self.client.get('/all_breakdowns/details/%s' % breakdown_id)

        self.assertEqual(response.context['breakdown'], breakdown)

    @skip
    @patch('breakdowns.filters.testFilter')
    def test_BreakdownFilter_called(self, test_mock):
        test_mock.form = BreakdownForm()
        self.client.get('/test')
        test_mock.assert_called_once()
