from django.shortcuts import render
from .serializers import PostSerializer,VoteSerializer
from .models import Post, Vote
from rest_framework import exceptions
from rest_framework import generics, permissions
# Create your views here.

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
     
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise exceptions.ValidationError("You have already voted for this post")
        serializer.save(voter=self.request.user,post=Post.objects.get(pk=self.kwargs['pk']))