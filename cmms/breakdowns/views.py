from django.shortcuts import render
from django.http import HttpResponse

from .forms import BreakdownForm

# Create your views here.


def home_page(request):
    form = BreakdownForm()

    if request.method == 'POST':
        form = BreakdownForm(data=request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'breakdowns/home.html', {
        "form": form,
    })
