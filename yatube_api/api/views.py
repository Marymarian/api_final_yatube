from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Group, Post, User
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .permission import IsAuthorOrReadOnly
from .serializers import CommentSerializer, FollowSerializer
from .serializers import GroupSerializer, PostSerializer
from rest_framework import mixins


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FollowViewSet( mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'post']
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
