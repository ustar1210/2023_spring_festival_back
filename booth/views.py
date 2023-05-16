from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from .models import *
from .serializers import BoothListSerializer, BoothDetailSerializer
from rest_framework.response import Response
import random
# Create your views here.

class BoothViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
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
        booths=Booth.objects.all()
        first=0
        second=0
        third=0
        for b in booths:
            if first == 0:
                first = b
            else :
                if b.like_cnt() >= first.like_cnt():
                    second = first
                    first = b
                else : 
                    if second == 0:
                        second = b
                    else : 
                        if second.like_cnt() <= b.like_cnt() :
                            third = second
                            second = b
                        else :
                            if third == 0:
                                third = b
                            else :
                                if third.like_cnt() <= b.like_cnt():
                                    third = b
                                else:
                                    pass
        hot_booths = [first, second, third]
        hot_booths_serializer = BoothListSerializer(hot_booths, many=True)
        return Response(hot_booths_serializer.data)
    
    @action(methods=["GET"], detail=False)
    def recommend(self, request):
        ran_booth = Booth.objects.all().order_by('?')[:2]
        ran_booth_serializer = BoothListSerializer(ran_booth, many=True)
        return Response(ran_booth_serializer.data)
        

