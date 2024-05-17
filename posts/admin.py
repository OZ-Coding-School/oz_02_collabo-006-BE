from django.contrib import admin
from .models import Post, HashtagPost, Like

# 게시글 admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

# 게시글-해시태그 중간테이블 admin
@admin.register(HashtagPost)
class HashtagPostAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass