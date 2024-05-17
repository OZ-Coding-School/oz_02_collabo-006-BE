from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Comment
from posts.models import Post
from users.serializers import UserSerializer

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(ModelSerializer):
    # 현재 사용자 정보 표시
    user = UserSerializer(read_only=True)
    # 댓글이 속한 게시물 지정, 표시
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = '__all__'

        # 부모 댓글을 선택적 필드로 설정
        extra_kwargs = {
            'parent_comment': {'required': False}
        }

    # 새로운 댓글 생성
    def create(self, validated_data):
        # 댓글이 속한 게시물 추가
        validated_data['post'] = Post.objects.get(id=self.initial_data['post'])
        # 요청을 보낸 사용자 추가
        validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)