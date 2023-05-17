from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from .models import *
from .serializers import BoothListSerializer, BoothDetailSerializer, LikeSerializer
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
        

    @action(methods=["POST", "DELETE"], detail=True, url_path='likes')
    def manage_like(self, request, pk=None):
        booth = self.get_object()
        booth_id = str(booth.id)
        if request.method == "POST":
            if booth_id in request.COOKIES.keys():
                return Response({'error': '이미 좋아요를 누르셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            key = create_random_number()
            like = Like.objects.create(booth=booth, key=key)
            serializer = LikeSerializer(like)
            response = Response(serializer.data)
            response.set_cookie(str(booth.id), key, max_age=None, expires=None)
            return response
        else:
            if booth_id not in request.COOKIES.keys():
                return Response({'error': '좋아요가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            key = request.COOKIES[booth_id]
            like = Like.objects.filter(booth=booth, key=key)
            if like.exists():
                like.delete()
                response = Response({'message': '좋아요 취소 완료'}, status=status.HTTP_204_NO_CONTENT)
                response.delete_cookie(str(booth.id))
                return response
            else:
                return Response({'error': '해당 부스에 대한 좋아요를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)