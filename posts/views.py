from django.shortcuts import render
from .serializers import PostSerializer
from .models import Post, Vote
from rest_framework import generics, permissions
# Create your views here.

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

class VoteCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
     
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(user=user, post=post)

    def perform_create(self, serializer):
        serializer.save(voter=self.request.user,post=Post.objects.get(pk=self.kwargs['pk']))