from django.shortcuts import render
from rest_framework import viewsets, filters
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .serializers import *
from fonts.models import *

# Create your views here.
class FamilyAPI(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    queryset = Family.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

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

def family(request, fam):
    # fonts = Font.objects.filter(
    #     family__name__contains=family).order_by('name')
    family = Family.objects.get(pk=fam)
    context = {
        "family": family,
    }
    return render(request, "family.html", context)