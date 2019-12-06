from django.contrib import admin
from django.urls import path, include
from .serializers import *
from fonts import views

urlpatterns = [
    path("", views.fonts, name="fonts"),
    # path("search/", views.search, name="search"),
    path("<str:pk>/", views.font_detail, name="font_detail"),
    # path("font_matcher/", views.match_font, name="match_font")
    # path("families/", views.families, name="families"),
    # path("weights/", views.weights, name="weights"),
    # path('<weight>/', views.font_weight, name="font_weight"),
    # path('<family>/', views.font_family, name="font_family"),
    # path("categories/", views.categories, name="categories"),
    # path('<category>/', views.font_category, name="font_category"),
    # path('recommender/', views.recommender, name='recommender')
]