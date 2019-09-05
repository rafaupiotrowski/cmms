from django import forms
from django.forms import ModelForm
from django.core.validators import MaxValueValidator
from django.utils import timezone

from bootstrap_datepicker_plus import DateTimePickerInput

from .models import Breakdown


class BreakdownForm(ModelForm):

    class Meta:
        model = Breakdown
        fields = ['machine', 'start_time', 'end_time']

    start_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=DateTimePickerInput(options={'format': 'YYYY-MM-DD HH:mm'}),
        validators=[MaxValueValidator(timezone.now())]
        )

    end_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=DateTimePickerInput(options={'format': 'YYYY-MM-DD HH:mm'}),
        validators=[MaxValueValidator(timezone.now())])

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time > timezone.now():
            raise forms.ValidationError('date_from_future!')
        return start_time

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and (start_time > end_time):
            raise forms.ValidationError(
                'End time before start time'
            )
