from django.contrib import admin
from .models import Post, HashtagPost

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(HashtagPost)
class HashtagPostAdmin(admin.ModelAdmin):
    pass