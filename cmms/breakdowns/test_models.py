from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_datetime
from django.utils import timezone

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
        breakdown = Breakdown.objects.create(machine=machine)
        self.assertIn(breakdown, machine.breakdown_set.all())

    def test_breakdown_saves_start_time(self):
        machine = Machine.objects.create(name='Machine 1')
        breakdown = Breakdown.objects.create(
            machine=machine,
            start_time=timezone.make_aware(parse_datetime('2000-01-01 12:00:00'))
            )
        self.assertEqual(
            breakdown.start_time,
            timezone.make_aware(parse_datetime('2000-01-01 12:00:00'))
            )
