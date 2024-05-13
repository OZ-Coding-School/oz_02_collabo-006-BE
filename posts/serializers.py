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


from rest_framework import serializers
from hashtags.models import Hashtag

class PostCreateSerializer(serializers.ModelSerializer):
    hashtag = serializers.CharField(write_only=True)

    class Meta:
        model = Post
        fields = ['content', 'comment_ck', 'visible', 'hashtag']

    def create(self, validated_data):
        hashtag_data = validated_data.pop('hashtag', None)
        post = Post.objects.create(**validated_data)
        if hashtag_data:
            # Split the hashtag string and remove duplicate hashtags
            hashtags = set(tag.strip() for tag in hashtag_data.split('#') if tag.strip())
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(content=tag)
                HashtagPost.objects.create(post=post, hashtag=hashtag)
        return post