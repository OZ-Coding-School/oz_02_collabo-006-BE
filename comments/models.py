from django.db import models
from common.models import CommonModel
from posts.models import Post
from users.models import User

class Comment(CommonModel):
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)

    # 대댓글을 위한 칼럼 -> 상위 댓글이 삭제되어도 대댓글은 유지
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    # Post:Comment => 1:N
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # User:Comment => 1:N
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.content
    
# 댓글 좋아요 테이블
class CommentLike(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_user_comment')
        ]