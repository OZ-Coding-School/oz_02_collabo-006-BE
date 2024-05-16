from django.urls import path
from .views import (
    CommentCreate
    )

urlpatterns = [
    path('<int:post_id>/create/', CommentCreate.as_view(), name='comment-create'),
]