from rest_framework import viewsets, generics
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models
from . serializers import ReplySerializer, TweetSerializer, ReplyStraightSerializer
from .permissions import IsAuthorOrIsAuthenticated


class TweetViewSet(viewsets.ModelViewSet):
    queryset = models.Tweet.objects.all()
    serializer_class = TweetSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthorOrIsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = models.Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthorOrIsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


# class TweetReplyViewSet(viewsets.ModelViewSet):
#     queryset = models.Reply.objects.all()
#     serializer_class = ReplySerializer
#     authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthorOrIsAuthenticated]
#
#     def list(self, request, *args, **kwargs):
#         tweet = models.Tweet.objects.get(pk=kwargs.get('pk'))
#         reply_queryset = tweet.replies.all()
#         serializer = ReplyStraightSerializer(reply_queryset, many=True)
#         return Response(serializer.data)
#
#     def perform_create(self, serializer):
#         serializer.save(profile=self.request.user.profile)



