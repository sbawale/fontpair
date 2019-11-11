from django.contrib import admin
from .models import FontPair # add this

class FontPairAdmin(admin.ModelAdmin):  # add this
  list_display = ('title', 'description', 'completed') # add this

# Register your models here.
admin.site.register(FontPair, FontPairAdmin) # add this