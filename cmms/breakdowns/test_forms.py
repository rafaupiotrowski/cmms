from django.test import TestCase
from django.utils.timezone import make_aware

from .forms import BreakdownForm
from .models import Machine

import sys


class BreakdownFormTest(TestCase):
    def test_breakdown_form_renders_dropdown_list(self):
        form = BreakdownForm()
        self.assertIn('select', form.as_p())

    def test_breakdown_form_lists_all_machines_to_choose_from(self):
        Machine.objects.create(name='Machine 1')
        all_machines = [machine.name for machine in Machine.objects.all()]
        form = BreakdownForm()

        choice_values, choice_names = zip(
            *form.fields['machine'].choices
            )
        self.assertEqual(all_machines, list(choice_names)[1:])

    def test_form_validation_for_correct_start_time(self):
        machine = Machine.objects.create(name='Machine 1')
        start_time = '2009-10-25 14:30'
        data = {'machine': machine.id, 'start_time': start_time}
        form = BreakdownForm(data)
        form.is_valid()
        self.assertTrue(form.is_valid())

    def test_form_does_not_validate_incorrect_start_time(self):
        machine = Machine.objects.create(name='Machine 1')
        start_time = '2009-10-25 14:30:30'
        data = {'machine': machine.id, 'start_time': start_time}
        form = BreakdownForm(data)
        form.is_valid()
        self.assertFalse(form.is_valid())

    def test_form_does_not_accept_start_time_in_future(self):
        pass
