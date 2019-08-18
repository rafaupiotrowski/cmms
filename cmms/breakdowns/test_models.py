from django.test import TestCase
from django.db.utils import IntegrityError

from .models import Machine, Breakdown


class MachineModelTest(TestCase):
    def test_default_name(self):
        machine = Machine.objects.create()
        self.assertEqual(machine.name, '')
        self.assertIsInstance(machine, Machine)

    def test_machines_names_are_unique(self):
        Machine.objects.create(name='Machine 1')
        with self.assertRaises(IntegrityError):
            Machine.objects.create(name='Machine 1')


class MachineBreakdownTest(TestCase):
    def test_breakdown_is_related_to_machine(self):
        machine = Machine.objects.create(name='Machine 1')
        breakdown = Breakdown()
        breakdown.machine = machine
        breakdown.save()
        self.assertEqual(machine, breakdown.machine)
