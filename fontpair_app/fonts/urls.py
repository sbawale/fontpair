from django.urls import path
from fonts import views

urlpatterns = [
    # path('fonts/', views.fonts, name='fonts'),
    path('', views.font_index, name="font_index"),
    path("<str:pk>/", views.font_detail, name="font_detail"),
]
