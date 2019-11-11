from django.shortcuts import render
from rest_framework import viewsets          # add this
from .serializers import FontPairSerializer      # add this
from .models import FontPair                     # add this

# Create your views here.

class FontPairView(viewsets.ModelViewSet):       # add this
  serializer_class = FontPairSerializer          # add this
  queryset = FontPair.objects.all()              # add this