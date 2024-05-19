from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Comment, CommentLike
from users.models import User
from posts.models import Post

class CommentSerializer(ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'parent_comment', 'post', 'user', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj).order_by('created_at')
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

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

# 좋아요 시리얼라이즈 -> 좋아요 생성
class CommentLikeSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all())
    comment_id = serializers.PrimaryKeyRelatedField(source='comment', queryset=Comment.objects.all())

    class Meta:
        model = CommentLike 
        fields = ['id', 'user_id', 'comment_id', 'created_at', 'updated_at']