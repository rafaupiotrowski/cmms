from django.shortcuts import render
from django.contrib import messages
from django.contrib.postgres.search import SearchVector

from .forms import BreakdownForm, SearchForm
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
    #form = SearchForm()
    form = BreakdownForm()
    last_breakdowns = Breakdown.objects.all().order_by('-end_time')[:5]
    return render(request, 'all_breakdowns.html', {
        'results': last_breakdowns,
        'form': form})


def breakdown_search(request):
    #form = SearchForm()
    form = BreakdownForm()
    query = None
    results = []
    if 'start_time' in request.GET:
        form = BreakdownForm(request.GET)
        if form.is_valid():
            print(form.cleaned_data)
            breakdown_description_query = form.cleaned_data['breakdown_description']
            results = Breakdown.objects.annotate(
#                search=SearchVector('breakdown_description')
            ).filter(
                breakdown_description__icontains=breakdown_description_query).order_by('-end_time')
        return render(request, 'all_breakdowns.html', {
                'form': form,
                'query': query,
                'results': results})
