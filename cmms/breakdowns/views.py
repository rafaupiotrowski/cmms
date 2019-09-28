from django.shortcuts import render
from django.contrib import messages

from .forms import BreakdownForm
from .models import Breakdown

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
    last_breakdowns = Breakdown.objects.all().order_by('-end_time')[:5]
    return render(request, 'all_breakdowns.html', {
        'last_breakdowns': last_breakdowns, })
