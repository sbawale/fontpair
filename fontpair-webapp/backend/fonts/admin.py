from django.contrib import admin
from .models import *

# Register your models here.
class FontAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'category', 'is_body', 'is_serif', 'is_italic', 'weight', 'url')
    list_filter = ['category', 'family']
    ordering = ('name',)

admin.site.register(FontPair)
admin.site.register(Font, FontAdmin)