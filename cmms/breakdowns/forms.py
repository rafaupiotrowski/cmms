from django import forms
from django.forms import ModelForm


from .models import Machine


class BreakdownForm(forms.Form):
    machine = forms.ModelChoiceField(queryset=Machine.objects.all())
