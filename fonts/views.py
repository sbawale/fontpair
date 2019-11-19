# from django.shortcuts import render
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from fonts.models import *


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

# ********************** Attribute Views **********************

# *********** FAMILIES ***********
def families(request):
    families = Family.objects.all().order_by('name')
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

# *********** CATEGORIES ***********
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
