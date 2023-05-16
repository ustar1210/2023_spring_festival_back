from rest_framework import serializers
from .models import *

class BoothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth
        fields = [
            "name",
            "type",
            "operator",
            "start_at",
            "end_at",
            "location",
            "description",
            "menu",
            "concept"
            ]