from rest_framework import viewsets

from . import models
from . import serializers


class TweetViewSet(viewsets.ModelViewSet):
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetSerializer


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = models.Reply.objects.all()
    serializer_class = serializers.ReplySerializer
