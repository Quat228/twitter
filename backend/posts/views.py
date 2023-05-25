from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions as p
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from . import models
from . import serializers
from . import permissions
from . import paginations

# p - REST permissions
# permission - Custom permissions


class TweetViewSet(viewsets.ModelViewSet):
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetSerializer
    permission_classes = [permissions.IsAuthorOrIsAuthenticated, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # pagination_class = paginations.TweetNumberPagination
    pagination_class = LimitOffsetPagination
    search_fields = ['text', 'profile__user__username']
    ordering_fields = ['updated_at', 'profile__user_id']

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(methods=['GET'], detail=False,
            serializer_class=serializers.TweetSerializer,
            permission_classes=[p.IsAuthenticated]
            )
    def recent_5(self, request, pk=None):
        serializer = self.serializer_class(
            self.get_queryset().filter(created_at__gte=timezone.now()-timezone.timedelta(days=5)), many=True)
        return Response(serializer.data, status=200)

    @action(methods=['POST'], detail=True,
            serializer_class=serializers.ReactionSerializer,
            permission_classes=[p.IsAuthenticated],
            )
    def reaction(self, request, pk=None):
        serializer = serializers.ReactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                profile=self.request.user.profile,
                tweet=self.get_object()
            )
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


# class ReplyViewSet(viewsets.ModelViewSet):
#     queryset = models.Reply.objects.all()
#     serializer_class = serializers.ReplySerializer
#     permission_classes = [permissions.IsAuthorOrIsAuthenticated]
#
#     def get_queryset(self):
#         return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])
#
#     def perform_create(self, serializer):
#         tweet_id = self.kwargs['tweet_id']
#         tweet = models.Tweet.objects.get(id=tweet_id)
#         serializer.save(tweet=tweet)


class ReplyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Reply.objects.all()
    serializer_class = serializers.ReplySerializer
    permission_classes = [permissions.IsAuthorOrIsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])


class ReplyListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Reply.objects.all()
    serializer_class = serializers.ReplySerializer
    permission_classes = [permissions.IsAuthorOrIsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text']
    ordering_fields = ['updated_at']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile, tweet_id=self.kwargs['tweet_id'])


class ReactionTypeViewSet(viewsets.ModelViewSet):
    queryset = models.ReactionType.objects.all()
    serializer_class = serializers.ReactionTypeSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class ReactionCreateAPIView(generics.CreateAPIView):
    queryset = models.Reaction.objects.all()
    serializer_class = serializers.ReactionSerializer
    permission_classes = [p.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            tweet_id=self.kwargs['tweet_id']
        )


class ReplyReactionCreateAPIView(generics.CreateAPIView):
    queryset = models.ReplyReaction.objects.all()
    serializer_class = serializers.ReplyReactionSerializer
    permission_classes = [p.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            reply=get_object_or_404(models.Reply, pk=self.kwargs['reply_id'])
        )
