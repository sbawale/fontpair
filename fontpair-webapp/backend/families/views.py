from django.shortcuts import render
from rest_framework import viewsets
from .models import *

# Create your views here.
# *********** FAMILIES ***********
def families(request):
    families = Family.objects.all().order_by('family_name')
    context = {
        'families': families
    }
    return render(request, 'families.html', context)

def font_family(request, family):
    fonts = Font.objects.filter(
        families__name__contains=family).order_by('name')
    context = {
        "family": family,
        "fonts": fonts
    }
    return render(request, "font_family.html", context)