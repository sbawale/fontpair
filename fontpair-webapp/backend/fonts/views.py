from django.shortcuts import render
from rest_framework import viewsets          # add this
from .serializers import *
from .models import *

# Create your views here.

class TodoView(viewsets.ModelViewSet):       # add this
      serializer_class = TodoSerializer          # add this
      queryset = Todo.objects.all()


# ********************** Recommender Views **********************
def font_recommendation_list(request):
    return render(request, 'font_recommendation_list.html')

def recommender(request):
    fonts = Font.objects.all().order_by('name')
    context = {
        'fonts': fonts
    }
    return render(request, 'recommender.html', context)


# ********************** Individual Fonts **********************
def fonts(request):
    fonts = Font.objects.all().order_by('name')
    context = {
        'fonts': fonts
    }
    return render(request, 'fonts.html', context)

def font_detail(request, pk):
    font = Font.objects.get(pk=pk)
    context = {
        'font': font
    }
    return render(request, 'font_detail.html', context)

# *********** WEIGHTS ***********
def weights(request):
    weights = Weight.objects.all().order_by('weight')
    context = {
        'weights': weights
    }
    return render(request, 'weights.html', context)

def font_weight(request, weight):
    fonts = Font.objects.filter(
        weights__weight__contains=weight).order_by('weight')
    context = {
        "weight": weight,
        "fonts": fonts
    }
    return render(request, "font_weight.html", context)