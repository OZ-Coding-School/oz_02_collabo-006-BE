from rest_framework import serializers
from users.models import User
from posts.models import Post
from hashtags.models import Hashtag

class HashtagSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['content']

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class PostSearchSerializer(serializers.ModelSerializer):
    user = UserSearchSerializer(read_only=True)
    hashtag = HashtagSearchSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['user', 'content', 'hashtag']
