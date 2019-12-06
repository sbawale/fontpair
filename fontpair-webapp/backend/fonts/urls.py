from django.contrib import admin
from django.urls import path, include
from .serializers import *
from fonts import views

urlpatterns = [
    path("", views.fonts, name="fonts"),
    # path("search/", views.search, name="search"),
    path("<str:pk>/", views.font_detail, name="font_detail"),
]