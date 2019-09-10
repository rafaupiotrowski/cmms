from django.test import TestCase

from .forms import BreakdownForm
from .models import Machine, Breakdown

import sys


class BreakdownFormTest(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(name='Machine 1')
        self.start_time = '2009-10-25 14:30'
        self.end_time = '2009-10-25 15:30'
        self.breakdown_description = 'test_description'
        self.correct_data = {
            'machine': self.machine.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'breakdown_description': self.breakdown_description}

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
        data = self.correct_data
        form = BreakdownForm(data)
#        self.assertTrue(form.is_valid())
        if not form.is_valid():
            print('formularz: ', form)
            print('dane: ', form.cleaned_data)
            print('błędy: ', form.errors)
        new_breakdown = form.save()
        self.assertEqual(new_breakdown, Breakdown.objects.all()[0])

    def test_form_does_not_accept_start_time_in_future(self):
        data = self.correct_data
        start_time_in_future = '3009-10-25 14:30'
        data['start_time'] = start_time_in_future
        incorrect_data = data
        form = BreakdownForm(incorrect_data)
        self.assertFalse(form.is_valid())

    def test_form_does_not_accept_end_time_in_future(self):
        data = self.correct_data
        end_time_in_future = '3009-10-25 14:30'
        data['end_time'] = end_time_in_future
        incorrect_data = data
        form = BreakdownForm(incorrect_data)
        self.assertFalse(form.is_valid())

    def test_for_start_time_before_end_time(self):
        data = self.correct_data
        start_time = '2009-10-25 14:30'
        end_time = '2009-10-24 15:30'
        data['start_time'] = start_time
        data['end_time'] = end_time
        incorrect_data = data
        form = BreakdownForm(incorrect_data)
        self.assertFalse(form.is_valid())

    def test_form_validation_for_blank_breakdown_description(self):
        data = self.correct_data
        blank_description = ''
        data['breakdown_description'] = blank_description
        incorrect_data = data
        form = BreakdownForm(incorrect_data)
        self.assertFalse(form.is_valid())
