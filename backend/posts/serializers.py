from rest_framework import serializers

from django.db.utils import IntegrityError

from . import models


class TweetSerializer(serializers.ModelSerializer):
    # reactions = serializers.ReadOnlyField(source='get_reactions')
    all_reactions = serializers.ReadOnlyField()  # source не нужен

    class Meta:
        model = models.Tweet
        fields = '__all__'
        read_only_fields = ['profile']


class ReplySerializer(serializers.ModelSerializer):
    all_reactions = serializers.ReadOnlyField(source='get_reactions')

    class Meta:
        model = models.Reply
        fields = '__all__'
        read_only_fields = ['profile', 'tweet']


class ReactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactionType
        fields = "__all__"


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reaction
        fields = '__all__'
        read_only_fields = ['profile', 'tweet']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            new_reaction_type = validated_data.pop('type')
            instance = self.Meta.model.objects.get(**validated_data)
            instance.type = new_reaction_type
            instance.save()
            return instance


class ReplyReactionSerializer(ReactionSerializer):
    class Meta:
        model = models.ReplyReaction
        fields = '__all__'
        read_only_fields = ['profile', 'reply']
