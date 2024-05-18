from django.urls import path
from .views import (
    CommentCreate,
    CommentRead,
    CommentUpdate,
    CommentDelete
    )

urlpatterns = [
    path('<int:post_id>/create/', CommentCreate.as_view(), name='comment-create'),
    path('<int:post_id>/', CommentRead.as_view(), name='comment-read'),
]