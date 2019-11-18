from rest_framework import serializers
from fonts.models import Font

class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        # fields = ('name', 'family', 'category', 'is_body', 'is_serif', 'is_italic', 'weight', 'url')
        fields = '__all__'