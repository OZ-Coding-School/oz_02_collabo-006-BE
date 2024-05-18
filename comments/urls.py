from django.urls import path
from .views import (
    CommentCreate,
    CommentRead,
    CommentUpdate,
    CommentDelete,
    CommentLikeView
    )

urlpatterns = [
    path('<int:post_id>/create/', CommentCreate.as_view(), name='comment-create'),
    path('<int:post_id>/', CommentRead.as_view(), name='comment-read'),
    path('<int:comment_id>/update/', CommentUpdate.as_view(), name='comment-update'),
    path('<int:comment_id>/delete/', CommentDelete.as_view(), name='comment-delete'),
    path('like/', CommentLikeView.as_view(), name='comment-like'),
]