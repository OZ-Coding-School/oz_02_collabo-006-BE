from rest_framework.serializers import ModelSerializer
from .models import Post
from users.serializers import UserSerializer
from comments.serializers import CommentSerializer
from medias.serializers import MediaSerializer
from hashtags.serializers import HashtagSerializer

class PostSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    hashtag = HashtagSerializer(many=True, required=False)
    media_set = MediaSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

class PostDetailSerializer(ModelSerializer):
    # Post:User => Post(FK) -> User
    user = UserSerializer(read_only=True)
    # Post:Comment => Post -> Comment(FK)
    comment_set = CommentSerializer(many=True, read_only=True)
    # Post:Media => Post -> Media(FK)
    media_set = MediaSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'