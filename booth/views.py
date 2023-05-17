from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from .models import *
from .serializers import BoothListSerializer, BoothDetailSerializer
from rest_framework.response import Response
from django.db.models import Count
# Create your views here.

class BoothViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(like_cnt=Count('likes'))
        return queryset
    
    queryset = Booth.objects.all()
    
    serializer_class = BoothListSerializer
    detail_serializer_class = BoothDetailSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()


    @action(methods=["GET"], detail=False)
    def hot(self, request):
        hot_booths = self.get_queryset().order_by('-like_cnt')[:3]
        hot_booths_serializer = BoothListSerializer(hot_booths, many=True)
        return Response(hot_booths_serializer.data)
    

    @action(methods=["GET"], detail=False)
    def recommend(self, request):
        ran_booth = self.get_queryset().order_by('?')[:2]
        ran_booth_serializer = BoothListSerializer(ran_booth, many=True)
        return Response(ran_booth_serializer.data)
        

