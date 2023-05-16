from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from .models import *
from .serializers import BoothSerializer
from rest_framework.response import Response

# Create your views here.

class BoothViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = BoothSerializer
    queryset = Booth.objects.all()

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
                if b.like_count() >= first.like_count():
                    second = first
                    first = b
                else : 
                    if second == 0:
                        second = b
                    else : 
                        if second.like_count() <= b.like_count() :
                            third = second
                            second = b
                        else :
                            if third == 0:
                                third = b
                            else :
                                if third.like_count() <= b.like_count():
                                    third = b
                                else:
                                    pass
        hot_booths = [first, second, third]
        hot_booths_serializer = BoothSerializer(hot_booths, many=True)
        return Response(hot_booths_serializer.data)