from rest_framework.serializers import ModelSerializer
from .models import Post, HashtagPost
from users.serializers import UserSerializer
from comments.serializers import CommentSerializer
from medias.serializers import MediaSerializer

class HashtagPostSerializer(ModelSerializer):
    class Meta:
        model = HashtagPost
        fields = '__all__'

class PostListSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    hashtag_post = HashtagPostSerializer(many=True, required=False)
    media_set = MediaSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

class PostDetailSerializer(ModelSerializer):
    # Post:User => Post(FK) -> User
    user = UserSerializer(read_only=True)
    # ManyToManyField -> 중간 모델인 HashtagPost로 관리
    hashtag_post = HashtagPostSerializer(many=True, required=False)
    # Post:Comment => Post -> Comment(FK)
    comment_set = CommentSerializer(many=True, read_only=True)
    # Post:Media => Post -> Media(FK)
    media_set = MediaSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'