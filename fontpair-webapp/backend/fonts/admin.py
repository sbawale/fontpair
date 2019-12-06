from django.contrib import admin
from .models import *

# Register your models here.
class FontAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'category', 'is_body', 'is_serif', 'is_italic', 'weight_num')
    list_filter = ['category', 'is_body', 'is_serif', 'is_italic']
    search_fields = ('name', 'family', 'category', )
    ordering = ('name',)

# admin.site.register(FontPair)
# admin.site.register(Weight)
admin.site.register(Font, FontAdmin)