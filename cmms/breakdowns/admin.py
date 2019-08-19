from django.contrib import admin

from .models import Machine, Breakdown

# Register your models here.
admin.site.register(Machine)
admin.site.register(Breakdown)
