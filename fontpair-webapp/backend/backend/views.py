from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from fonts.models import *

# Create your views here.
def index(request):
    fonts = Font.objects.all()
    context = {
        'fonts':fonts
    }
    return render(request, 'index.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)