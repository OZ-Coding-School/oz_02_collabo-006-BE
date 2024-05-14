from rest_framework.serializers import ModelSerializer
from .models import Post, HashtagPost
from users.serializers import UserSerializer
from comments.serializers import CommentSerializer
from medias.serializers import MediaSerializer
from hashtags.models import Hashtag
from rest_framework import serializers

# HashtagPost 중간 테이블 시리얼라이즈
class HashtagPostSerializer(ModelSerializer):
    class Meta:
        model = HashtagPost
        fields = '__all__'

# 게시글 리스트 시리얼라이즈
class PostListSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    hashtag_post = HashtagPostSerializer(many=True, required=False)
    media_set = MediaSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

# 특정 게시글 시리얼라이즈
class PostDetailSerializer(ModelSerializer):
    # Post:User => Post(FK) -> User
    user = UserSerializer(read_only=True)
    # ManyToManyField -> 중간 모델인 HashtagPost로 관리
    hashtag_post = HashtagPostSerializer(many=True, required=False)
    # Post:Comment => Post -> Comment(FK)
    comment_set = CommentSerializer(many=True, read_only=True)
    # Post:Media => Post -> Media(FK)
    media_set = MediaSerializer(many=True)

    # Post, Hashtag -> ManyToManyField 관계 처리
    hashtag = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    # 게시글과 연결된 해시태그 가져오기
    def get_hashtag(self, post):
        hashtags = post.hashtag.all()
        return [hashtag.content for hashtag in hashtags]

# 게시글 생성 시리얼라이즈
class PostCreateSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    hashtag_post = HashtagPostSerializer(many=True, required=False)
    media_set = MediaSerializer(many=True, required=False)
    hashtag = serializers.CharField(write_only=True, allow_blank=True, required=False) # 해시태그를 받는 필드

    class Meta:
        model = Post
        fields = '__all__'

    # 해시태그 생성
    def create(self, validated_data):
        # hashtag 추출, 나머지 필드는 그대로 둠
        hashtag_data = validated_data.pop('hashtag', None)
        post = Post.objects.create(**validated_data)
        if hashtag_data:
            # 해시태그 문자열 '#'으로 구분 후, 리스트로 변환하고 중복 제거
            hashtags = set(tag.strip() for tag in hashtag_data.split('#') if tag.strip())
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(content=tag)
                # 게시글과 해시태그 간의 관계를 나타내는 객체 생성
                HashtagPost.objects.create(post=post, hashtag=hashtag)
        return post
