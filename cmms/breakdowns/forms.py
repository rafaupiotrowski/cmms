from django import forms
from django.forms import ModelForm
from django.core.validators import MaxValueValidator
from django.utils import timezone


from .models import Breakdown


class BreakdownForm(ModelForm):

    class Meta:
        model = Breakdown
        fields = ['machine', 'start_time', 'end_time']

    start_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        validators=[MaxValueValidator(timezone.now())])

    end_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        validators=[MaxValueValidator(timezone.now())])
