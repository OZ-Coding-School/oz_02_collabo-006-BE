from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Comment
from users.models import User
from posts.models import Post
from users.serializers import UserSerializer

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'parent_comment', 'content']

        # parent_comment 필드를 선택적 필드로 설정합니다.
        extra_kwargs = {
            'parent_comment': {'required': False}
        }