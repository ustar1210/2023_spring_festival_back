from django.urls import include, path
from rest_framework import routers
from .views import *

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("booths", BoothViewSet, basename="booths")

urlpatterns = [
    path("", include(default_router.urls)),
]
