from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import *
from .serializers import *

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

def category(request, cat):
    # Use lists of families instead
    categories = Category.objects.filter(name=cat)
    context = {
        "categories": categories
    }
    return render(request, "category.html", context)