from .models import Breakdown

from bootstrap_datepicker_plus import DatePickerInput

import django_filters

from .forms import BreakdownForm


class BreakdownFilter(django_filters.FilterSet):
    breakdown_description = django_filters.CharFilter(lookup_expr='icontains')
    start_time = django_filters.DateTimeFilter(
        widget=DatePickerInput(options={'format': 'YYYY-MM-DD'}),
        lookup_expr='gt')
    end_time = django_filters.DateTimeFilter(
            widget=DatePickerInput(options={'format': 'YYYY-MM-DD'}),
            lookup_expr='lt')

    class Meta:
        model = Breakdown
        fields = ['machine', 'start_time', 'end_time', 'breakdown_description']


class testFilter():
    x='xyz'
    form = BreakdownForm()
