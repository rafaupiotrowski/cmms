from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    def setUp(self):
        self.machine = Machine.objects.create(name='Machine 1')

    def test_breakdown_is_related_to_machine(self):
        breakdown = Breakdown.objects.create(machine=self.machine)
        self.assertIn(breakdown, self.machine.breakdown_set.all())

    def test_breakdown_saves_start_time(self):
        start_time = timezone.make_aware(parse_datetime('2000-01-01 12:00:00'))
        breakdown = Breakdown.objects.create(
            machine=self.machine, start_time=start_time)

        self.assertEqual(breakdown.start_time, start_time)

    def test_breakdown_saves_end_time(self):
        end_time = timezone.make_aware(parse_datetime('2000-01-01 12:00:00'))
        breakdown = Breakdown.objects.create(
            machine=self.machine, end_time=end_time)

        self.assertEqual(breakdown.end_time, end_time)

    def test_breakdown_description_cannot_be_empty(self):
        breakdown = Breakdown.objects.create(
            machine=self.machine,
            breakdown_description='')
        with self.assertRaises(ValidationError):
            breakdown.save()
            breakdown.full_clean()

    def test_breakdown_string_represantation(self):
        start_time = timezone.make_aware(parse_datetime('2000-01-01 12:00:00'))
        end_time = timezone.make_aware(parse_datetime('2000-01-01 13:00:00'))
        description = 'Test breakdown'
        breakdown = Breakdown.objects.create(
            machine=self.machine, start_time=start_time, end_time=end_time,
            breakdown_description=description)
        breakdown_as_string = '''Machine: Machine 1
                                breakdown_description: Test breakdown
                                start time: 2000-01-01 12:00:00+01:00
                                end time: 2000-01-01 13:00:00+01:00'''\
                                .replace(' ', '')

        self.assertEqual(
                        breakdown.__str__().replace(' ', ''),
                        breakdown_as_string)
