from django.shortcuts import render
from django.http import HttpResponse

from .forms import BreakdownForm

# Create your views here.


def home_page(request):
    form = BreakdownForm()
    return render(request, 'breakdowns/home.html', {
        "form": form,
    })
