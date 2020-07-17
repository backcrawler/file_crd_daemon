from rest_framework import serializers
from .models import Pack


class PackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        fields = ['f']