from django.shortcuts import render
from django.contrib import messages

from .forms import BreakdownForm
from .models import Breakdown

# Create your views here.


def home_page(request):
    breakdown_form = BreakdownForm()
    last_breakdowns = Breakdown.objects.all()[:5]

    if request.method == 'POST':
        breakdown_form = BreakdownForm(data=request.POST)
        if breakdown_form.is_valid():
            breakdown_form.save()
            messages.success(request, 'Breakdown successfully saved.')
    return render(request, 'breakdowns/home.html', {
        "form": breakdown_form, 'last_breakdowns': last_breakdowns,
    })
