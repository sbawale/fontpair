from django.shortcuts import render
from rest_framework import viewsets
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .serializers import *
from fonts.models import *

# Create your views here.
class FamilyAPI(viewsets.ModelViewSet):
      serializer_class = FamilySerializer
      queryset = Family.objects.all()

def families(request):
    family_list = Family.objects.all().order_by('name')
    page = request.GET.get('page', 1)
    paginator = Paginator(family_list, 20)

    try:
        families = paginator.page(page)
    except PageNotAnInteger:
        families = paginator.page(1)
    except EmptyPage:
        families = paginator.page(paginator.num_pages)
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