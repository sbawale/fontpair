from django.contrib import admin
from django.urls import path, include
from .serializers import FontSerializer
from fonts import views

urlpatterns = [
    path("", views.fonts, name="fonts"),
    path("<str:pk>/", views.font_detail, name="font_detail"),
    # path("families/", views.families, name="families"),
    # path("weights/", views.weights, name="weights"),
    # path('<weight>/', views.font_weight, name="font_weight"),
    # path('<family>/', views.font_family, name="font_family"),
    # path("categories/", views.categories, name="categories"),
    # path('<category>/', views.font_category, name="font_category"),
    # path('recommender/', views.recommender, name='recommender')
]