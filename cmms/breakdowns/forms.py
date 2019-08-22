from django import forms
from django.forms import ModelForm


from .models import Breakdown


class BreakdownForm(ModelForm):

    #start_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])

    class Meta:
        model = Breakdown
        fields = ['machine', 'start_time']
