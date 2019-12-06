from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView
from rest_framework import viewsets, filters
import joblib
from .models import *
from .serializers import *

# Create your views here.

class FontAPI(viewsets.ModelViewSet):
    queryset = Font.objects.all()
    serializer_class = FontSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','^name','^family.name','^category.name']

def SearchResultsView(ListView):
    model = Font
    template_name = 'search_results.html'

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

    context = {
        'font': font,
        'recs_sim': recs_sim,
        'recs_diff': recs_diff
    }
    return render(request, 'font_detail.html', context)

# ********************** recommendations **********************
def font_recommendation_list(request):
    return render(request, 'font_recommendation_list.html')

def match_font(request):
    fonts = Font.objects.all().order_by('name')
    context = {
        'fonts': fonts
    }
    return render(request, 'match_font.html', context)

# *********** weights ***********
# def weights(request):
#     weights = Weight.objects.all().order_by('weight')
#     context = {
#         'weights': weights
#     }
#     return render(request, 'weights.html', context)

def weight(request, weight):
    fonts = Font.objects.filter(
        weights__weight__contains=weight).order_by('weight')
    context = {
        "weight": weight,
        "fonts": fonts
    }
    return render(request, "font_weight.html", context)