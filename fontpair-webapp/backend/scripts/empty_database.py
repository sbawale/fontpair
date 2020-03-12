from django.shortcuts import render
from fonts.models import *
from families.models import *
from categories.models import *

# Deletes all objects from all database tables

def run():
    Category.objects.all().delete()
    Family.objects.all().delete()
    Font.objects.all().delete()
