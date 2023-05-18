from django.urls import include, path
from rest_framework import routers
from .views import *

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("booths", BoothViewSet, basename="booths")
comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register("comments", CommentViewSet, basename="comments")
comment_reply_router = routers.SimpleRouter(trailing_slash=False)
comment_reply_router.register("replies",CommentReplyViewSet, basename="replies")

urlpatterns = [
    path("", include(default_router.urls)),
    path("booths/<int:id>/", include(comment_router.urls)),
    path("", include(comment_router.urls)),
    path("comments/<int:id>/", include(comment_reply_router.urls)),
    path("", include(comment_reply_router.urls)),
]
