from django.shortcuts import render
from django.contrib import messages

from bootstrap_datepicker_plus import DateTimePickerInput

from .forms import BreakdownForm

# Create your views here.


def home_page(request):
    breakdown_form = BreakdownForm()

    if request.method == 'POST':
        breakdown_form = BreakdownForm(data=request.POST)
        if breakdown_form.is_valid():
            breakdown_form.save()
            messages.success(request, 'Breakdown successfully saved.')
    return render(request, 'breakdowns/home.html', {
        "form": breakdown_form,
    })
