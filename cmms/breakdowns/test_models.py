from django.test import TestCase

from .models import Machine

class MachineModelTest(TestCase):

    def test_default_name(self):
        machine = Machine()
        self.assertEqual(machine.name, '')
