from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets
import joblib
from .models import *
from .serializers import *

# Create your views here.

class FontAPI(viewsets.ModelViewSet):
      serializer_class = FontSerializer
      queryset = Font.objects.all()

# ********************** Individual Fonts **********************
def fonts(request):
    font_list = Font.objects.all().order_by('name')
    style = 'regular' # could create a dictionary and use for loop to populate w/ italic values
    page = request.GET.get('page', 1)
    paginator = Paginator(font_list, 20)

    try:
        fonts = paginator.page(page)
    except PageNotAnInteger:
        fonts = paginator.page(1)
    except EmptyPage:
        fonts = paginator.page(paginator.num_pages)

    context = {
        'fonts': fonts
    }
    return render(request, 'fonts.html', context)

def font_detail(request, pk):
    # Load pickle files
    fonts = joblib.load('data/fonts.pkl')
    vectors = joblib.load('data/vectors.pkl')
    knn = joblib.load('data/knn.pkl')

    # Get specific font parameters for display
    font = Font.objects.get(pk=pk)
    recs_sim, recs_diff = Font.get_recommendations(font,fonts,vectors,knn,5)
    weight_num = font.numeric_weight()
    italic = font.italic()
    style = 'normal'

    if italic:
        style = 'italic'

    context = {
        'font': font,
        'recs_sim': recs_sim,
        'recs_diff': recs_diff,
        'weight_num': weight_num,
        'style': style
    }
    return render(request, 'font_detail.html', context)

# ********************** recommendations **********************
# def font_recommendation_list(request):
#     return render(request, 'font_recommendation_list.html')

# def recommender(request):
#     fonts = Font.objects.all().order_by('name')
#     context = {
#         'fonts': fonts
#     }
#     return render(request, 'recommender.html', context)

# *********** weights ***********
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