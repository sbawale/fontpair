from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index)
    path("", views.fonts, name="fonts"),
    path("<str:pk>/", views.font_detail, name="font_detail"),
    path("families/", views.families, name="families"),
    path('<family>/', views.font_family, name="font_family"),
    path("categories/", views.categories, name="categories"),
    path('<category>/', views.font_category, name="font_category"),
    path("weights/", views.weights, name="weights"),
    path('<weight>/', views.font_weight, name="font_weight"),
    path('recommender/', views.recommender, name='recommender')
]