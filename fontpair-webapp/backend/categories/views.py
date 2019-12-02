from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.

class CategoryAPI(viewsets.ModelViewSet):
      serializer_class = CategorySerializer
      queryset = Category.objects.all()

def categories(request):
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories
    }
    return render(request, 'categories.html', context)

def font_category(request, category):
    fonts = Font.objects.filter(
        categories__name__contains=category).order_by('name')
    context = {
        "category": category,
        "fonts": fonts
    }
    return render(request, "font_category.html", context)