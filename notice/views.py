from django.shortcuts import render
from rest_framework import mixins
from .models import *
from .serializers import *
from rest_framework import viewsets

class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()