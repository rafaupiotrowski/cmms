from django import forms
from django.forms import ModelForm

import sys

from .models import Machine

class BreakdownForm(forms.Form):

#    machines_count = len(Machine.objects.all())
#    machines_names = [machine.name for machine in Machine.objects.all()]

    machine = forms.ModelChoiceField(
        queryset=Machine.objects.all()
#        #choices = (("1", "Machine 1"), ("2", "Machine 2"))
#        choices = zip(
#                    range(machines_count),
#                    machines_names
#                    )
    )
