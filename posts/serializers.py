from rest_framework import serializers

from . import models


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tweet
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reply
        fields = '__all__'
