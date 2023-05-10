from rest_framework import serializers

from django.db.utils import IntegrityError

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
        read_only_fields = ['profile', 'tweet']


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reaction
        fields = '__all__'
        read_only_fields = ['profile', 'tweet']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            print(validated_data)
            new_reaction_type = validated_data.pop('reaction')
            print(new_reaction_type)
            instance = self.Meta.model.objects.get(**validated_data)
            instance.reaction = new_reaction_type
            instance.save()
            return instance


class ReactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactionType
        fields = "__all__"
