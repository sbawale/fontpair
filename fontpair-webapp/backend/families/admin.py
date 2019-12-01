from django.contrib import admin
from .models import *

# Register your models here.
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

admin.site.register(Family, FamilyAdmin)