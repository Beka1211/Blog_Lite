from django.db.models import F
from .models import Post, SubPost

from rest_framework import viewsets, permissions, status
from .serializers import PostSerializer, SubPostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAuthenticated]
            )
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        return Response({
            'liked': liked,
            'likes_count': post.likes.count()
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'],
            permission_classes=[permissions.AllowAny]
            )
    def view(self, request,pk=None):
        post = self.get_object()
        post.views_count = F('views_count') + 1
        post.save(update_fields=['views_count'])
        post.refresh_from_db()
        return Response({
            'views': post.views_count
        }, status=status.HTTP_200_OK)


class SubPostViewSet(viewsets.ModelViewSet):
    queryset = SubPost.objects.all()
    serializer_class = SubPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAuthenticated]
            )
    def like(self, request, pk=None):
        subpost = self.get_object()
        user = request.user
        if user in subpost.likes.all():
            subpost.likes.remove(user)
            liked = False
        else:
            subpost.likes.add(user)
            liked = True
        return Response({
            'liked': liked,
            'likes_count': subpost.likes.count()
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'],
            permission_classes=[permissions.AllowAny]
            )
    def view(self, request, pk=None):
        subpost = self.get_object()
        subpost.views_count = F('views_count') + 1
        subpost.save(update_fields=['views_count'])
        subpost.refresh_from_db()
        return Response({
            'views': subpost.views_count
        }, status=status.HTTP_200_OK)
