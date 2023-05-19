from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from .models import *

from .serializers import BoothListSerializer, BoothDetailSerializer, CommentSerializer, CommentReplySerializer, LikeSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone

# Create your views here.

class BoothViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    
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
        today = timezone.now()
        hot_booths = self.get_queryset().filter(start_at__lte=today, end_at__gte=today).order_by('-like_cnt')[:10]
        hot_booths_serializer = BoothListSerializer(hot_booths, many=True)
        return Response(hot_booths_serializer.data)

    @action(methods=["GET"], detail=False)
    def recommend(self, request):
        today = timezone.now()
        ran_booth = self.get_queryset().filter(start_at__lte=today, end_at__gte=today).order_by('?')[:2]
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


class CommentViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip_address=ip)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        password = request.data.get('password')
        if password == instance.password:
            instance.is_deleted=True
            instance.save()
            return Response({'message':'댓글이 삭제되었습니다.'})
        return Response(status=400)
    
class CommentReplyViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    serializer_class = CommentReplySerializer
    queryset = CommentReply.objects.all()

    def perform_create(self, serializer):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip_address=ip)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        password = request.data.get('password')
        if password == instance.password:
            instance.is_deleted=True
            instance.save()
            return Response({'message':'댓글 삭제'})
        return Response(status=400)
