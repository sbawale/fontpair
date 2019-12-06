from django.shortcuts import render
from rest_framework import viewsets, filters
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    category_list = Category.objects.all().order_by('name')
    page = request.GET.get('page', 1)
    paginator = Paginator(category_list, 10)

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
    context = {
        'categories': categories
    }
    return render(request, 'categories.html', context)

def category(request, pk):
    category = Category.objects.get(pk=pk)
    family_list = Family.objects.filter(category__pk=pk)
    page = request.GET.get('page', 1)
    paginator = Paginator(family_list, 20)

    try:
        families = paginator.page(page)
    except PageNotAnInteger:
        families = paginator.page(1)
    except EmptyPage:
        families = paginator.page(paginator.num_pages)
    context = {
        "category": category,
        "families": families
    }
    return render(request, 'category.html', context)