from django.test import TestCase

import sys

from .forms import BreakdownForm
from .models import Machine

class BreakdownFormTest(TestCase):
    def test_breakdown_form_renders_dropdown_list(self):
        form = BreakdownForm()
        self.assertIn('select', form.as_p())

    def test_breakdown_form_lists_all_machines_to_choose_from(self):
        Machine.objects.create(name='Machine 1')
#        Machine.objects.create(name='Machine 2')
        all_machines = [machine.name for machine in Machine.objects.all()]
        form = BreakdownForm()

        choice_values, choice_names = zip(
            *form.fields['machine'].choices
            )
        self.assertEqual(all_machines, list(choice_names)[1:])
