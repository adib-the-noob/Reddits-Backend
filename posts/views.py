from django.shortcuts import render
from .serializers import PostSerializer,VoteSerializer
from .models import Post, Vote
from rest_framework import exceptions,mixins,response,status
from rest_framework import generics, permissions
# Create your views here.

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)



class PostRetrive(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if post.poster != request.user:
            raise exceptions.PermissionDenied()
        return super().delete(request, *args, **kwargs)
        

class VoteCreate(generics.CreateAPIView,mixins.DestroyModelMixin):
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

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise exceptions.ValidationError("You have not voted for this post")
