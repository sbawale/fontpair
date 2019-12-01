from rest_framework import serializers
from .models import *

class FontSerializer(serializers.ModelSerializer):
  class Meta:
    model = Font
    fields = ('id', 'title', 'description', 'completed')