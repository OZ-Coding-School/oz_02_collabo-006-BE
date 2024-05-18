# archive/serializers.py
from rest_framework import serializers
from .models import Archive, ArchiveStatus, ArchivePost
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'
        read_only_fields = ['user', 'status']

class ArchiveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveStatus
        fields = '__all__'

class ArchivePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivePost
        fields = '__all__'


class ArchiveSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Archive
        fields = '__all__'
        read_only_fields = ['user', 'status']

    def get_posts(self, obj):
        archive_posts = ArchivePost.objects.filter(archive=obj)
        return [ArchivePostSerializer(archive_post).data['post'] for archive_post in archive_posts]