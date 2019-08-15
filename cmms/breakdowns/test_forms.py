from django.test import TestCase

from .forms import BreakdownForm

class BreakdownFormTest(TestCase):
    def test_breakdown_form_renders_dropdown_list(self):
        form = BreakdownForm()
        self.assertIn('select', form.as_p())
