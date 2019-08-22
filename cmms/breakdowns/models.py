from django.db import models
from django.utils import timezone

# Create your models here.


class Machine(models.Model):
    name = models.TextField(blank=False, default='', unique=True)

    def __str__(self):
        return self.name


class Breakdown(models.Model):
    machine = models.ForeignKey(
        Machine, default=None, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now())
