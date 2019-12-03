from django.shortcuts import render
from fonts.models import *
from families.models import *
from categories.models import *

def run():
    # Deletes all objects from Font, Families, and Categories database tables
    Font.objects.all().delete()
    Family.objects.all().delete()
    Category.objects.all().delete()
    # FontPair.objects.all().delete()
    # Weight.objects.all().delete()