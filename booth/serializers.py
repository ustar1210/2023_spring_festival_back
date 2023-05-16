from rest_framework import serializers
from .models import *

class BoothListSerializer(serializers.ModelSerializer):
    
    like_cnt = serializers.SerializerMethodField()
    logo_image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        count = len(Like.objects.filter(booth=instance.pk))
        return count

    def get_logo_image(self, instance):
        #아직 구현 안함
        return None
    
    def get_is_liked(self, instance):
        #아직 구현 안함
        return None

    class Meta:
        model = Booth
        fields = [
            "id",
            "name",
            "type",
            "operator",
            "logo_image",
            "like_cnt",
            "start_at",
            "end_at",
            "location",
            "is_liked",
        ]

class BoothDetailSerializer(serializers.ModelSerializer):
    
    like_cnt = serializers.SerializerMethodField()
    logo_image = serializers.SerializerMethodField()
    menu_image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        count = len(Like.objects.filter(booth=instance.pk))
        return count

    def get_logo_image(self, instance):
        #아직 구현 안함
        return None
    
    def get_menu_image(self, instance):
        #아직 구현 안함
        return None

    def get_is_liked(self, instance):
        #아직 구현 안함
        return None
    
    class Meta:
        model = Booth
        fields = [
            "id",
            "name",
            "type",
            "operator",
            "logo_image",
            "like_cnt",
            "start_at",
            "end_at",
            "location",
            "description",
            "menu",
            "menu_image",
            "concept",
            "is_liked",
            ]