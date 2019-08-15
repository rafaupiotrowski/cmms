from django import forms

from .models import Machine

class BreakdownForm(forms.Form):
    machine = forms.ChoiceField(
        choices = (("1", "Machine 1"), ("2", "Machine 2"))
    )
