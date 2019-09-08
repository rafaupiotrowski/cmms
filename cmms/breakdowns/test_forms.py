from django.test import TestCase

from .forms import BreakdownForm
from .models import Machine, Breakdown

import sys


class BreakdownFormTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.machine = Machine.objects.create(name='Machine 1')
#        self.start_time = '2009-10-25 14:30'

    def test_breakdown_form_renders_dropdown_list(self):
        form = BreakdownForm()
        self.assertIn('select', form.as_p())

    def test_breakdown_form_lists_all_machines_to_choose_from(self):
        all_machines = [machine.name for machine in Machine.objects.all()]
        form = BreakdownForm()

        choice_values, choice_names = zip(
            *form.fields['machine'].choices
            )
        self.assertEqual(all_machines, list(choice_names)[1:])

    def test_form_saved_if_data_correct(self):
        start_time = '2009-10-25 14:30'
        end_time = '2009-10-25 15:30'
        data = {'machine': self.machine.id, 'start_time': start_time,
                'end_time': end_time}
        form = BreakdownForm(data)
        if form.is_valid():
            new_breakdown = form.save()
        self.assertEqual(new_breakdown, Breakdown.objects.all()[0])

    def test_form_does_not_validate_incorrect_start_time(self):
        start_time = '2009-10-25 14:90'
        end_time = '2009-10-25 15:30'
        data = {'machine': self.machine.id, 'start_time': start_time,
                'end_time': end_time}
        form = BreakdownForm(data)
        self.assertFalse(form.is_valid())

    def test_form_does_not_accept_start_time_in_future(self):
        start_time = '3009-10-25 14:30'
        end_time = '2009-10-25 15:30'
        data = {'machine': self.machine.id, 'start_time': start_time,
                'end_time': end_time}
        form = BreakdownForm(data)
        self.assertFalse(form.is_valid())

    def test_form_does_not_accept_end_time_in_future(self):
        start_time = '2009-10-25 14:30'
        end_time = '3009-10-25 15:30'
        data = {'machine': self.machine.id, 'start_time': start_time,
                'end_time': end_time}
        form = BreakdownForm(data)
        self.assertFalse(form.is_valid())

    def test_for_start_time_before_end_time(self):
        start_time = '2009-10-25 14:30'
        end_time = '2009-10-24 15:30'
        data = {'machine': self.machine.id, 'start_time': start_time,
                'end_time': end_time}
        form = BreakdownForm(data)
        self.assertFalse(form.is_valid())
