from django.test import TestCase

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

    def test_form_validation_for_correct_start_datetime(self):
        machine = Machine.objects.create(name='Machine 1')
        start_datetime = '2006-10-25 14:30'
        form = BreakdownForm()
        data = {'machine': 2, 'start_datetime': start_datetime}
        form = BreakdownForm(data)
        form.is_valid()
        print(form.errors, file=sys.stderr)
        print(
            'choices:',
            form.fields['machine'].choices.queryset,
            file=sys.stderr)
        print('form: ', form.as_p(), file=sys.stderr)
        self.assertTrue(form.is_valid())
