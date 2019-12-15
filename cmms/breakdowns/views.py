from django.shortcuts import render
from django.contrib import messages

from .forms import BreakdownForm
from .models import Breakdown
from .filters import BreakdownFilter, testFilter

# Create your views here.


def home_page(request):
    breakdown_form = BreakdownForm()

    if request.method == 'POST':
        breakdown_form = BreakdownForm(data=request.POST)
        if breakdown_form.is_valid():
            breakdown_form.save()
            messages.success(request, 'Breakdown successfully saved.')
    return render(request, 'home.html', {
        "form": breakdown_form,
    })


def all_breakdowns(request):
    breakdown_list = Breakdown.objects.all().order_by('-end_time')
    breakdown_filter = BreakdownFilter(
        request.GET, queryset=breakdown_list)
    filter_form = breakdown_filter.form
    last_breakdowns = Breakdown.objects.all().order_by('-end_time')[:5]
    return render(request, 'all_breakdowns.html', {
        'last_breakdowns': last_breakdowns, 'filter': breakdown_filter,
        'form': filter_form, })


def details(request, breakdown_id):
    breakdown = Breakdown.objects.get(pk=breakdown_id)
    return render(
        request, 'breakdown_details.html',
        {'breakdown': breakdown})


def test(request):
    test_filter = testFilter()
    test_filter_form = test_filter.form
    return render(request, 'all_breakdowns.html', {
        'last_breakdowns': None, 'filter': None,
        'form': test_filter_form, })
