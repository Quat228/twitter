from rest_framework import serializers

from . import models


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tweet
        fields = '__all__'
        read_only_fields = ['profile']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reply
        fields = '__all__'
        read_only_fields = ['profile']


class ReplyStraightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reply
        fields = '__all__'
        read_only_fields = ['profile', 'tweet']
