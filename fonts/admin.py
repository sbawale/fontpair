from django.contrib import admin
from .models import *

# Register your models here.
class FontAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'category', 'is_body', 'is_serif', 'is_italic', 'weight', 'url')
    list_filter = ['category', 'family']
    ordering = ('name',)

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

class WeightAdmin(admin.ModelAdmin):
    list_display = ('string',)
    ordering = ('weight',)

admin.site.register(FontPair)
admin.site.register(Font, FontAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Weight, WeightAdmin)