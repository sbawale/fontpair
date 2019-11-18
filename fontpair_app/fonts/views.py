from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *

# Create your views here.
def fonts(request):
    return render(request, 'fonts.html', {})

def font_index(request):
    fonts = Font.objects.all()
    context = { 'fonts': fonts }
    return render(request, 'font_index.html', context)

def font_detail(request, pk):
    font = Font.objects.get(pk=pk)
    context = { 'font': font }
    return render(request, 'font_detail.html', context)

class FontView(viewsets.ModelViewSet):
    serializer_class = FontSerializer
    queryset = Font.objects.all()