from rest_framework import serializers
from .models import FontPair

class FontPairSerializer(serializers.ModelSerializer):
  class Meta:
    model = FontPair
    fields = ('id', 'title', 'description', 'completed')