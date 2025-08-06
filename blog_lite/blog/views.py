from django.shortcuts import render,redirect
from rest_framework import viewsets
from .models import Post, SubPost
from .serializers import PostSerializer, SubPostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SubPostViewSet(viewsets.ModelViewSet):
    queryset = SubPost.objects.all().order_by('-created_at')
    serializer_class = SubPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
