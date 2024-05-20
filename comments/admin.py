from django.contrib import admin
from .models import Comment, CommentLike

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    pass