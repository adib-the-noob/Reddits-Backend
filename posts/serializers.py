from .models import Post, Vote
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    class Meta:
        model = Post
        fields = ('title', 'url', 'poster', 'poster_id','created_at',)

class VoteSerializer(serializers.ModelSerializer):
    model = Vote
    fields = ['id',]