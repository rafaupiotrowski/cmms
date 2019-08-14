from django.shortcuts import render
from django.http import HttpResponse

from .models import Machine

# Create your views here.
def home_page(request):
    return render(request, 'breakdowns/home.html', {
        "all_machines": Machine.objects.all(),
    })
