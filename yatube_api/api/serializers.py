from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Post."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Group."""

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Follow."""
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны.'
            ),
        )

    def validate_following(self, value):
        """Невозможно подписаться на самого себя."""
        user = self.context['request'].user
        if value == user:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return value
