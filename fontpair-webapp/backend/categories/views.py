from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import *
from .serializers import *
from families.models import *
from fonts.models import *

# Create your views here.

class CategoryAPI(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

def categories(request):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories
    }
    return render(request, 'categories.html', context)

def category(request, pk):
    # Use lists of families instead
    category = Category.objects.get(pk=pk)
    families = Family.objects.filter(category__pk=pk)
    num_families = len(families)
    last_family = families[num_families-1]
    context = {
        "category": category,
        "families": families,
        "num_families": num_families,
        "last_family": last_family
    }
    return render(request, "category.html", context)