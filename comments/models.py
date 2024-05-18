from django.db import models
from common.models import CommonModel
from posts.models import Post
from users.models import User

class Comment(CommonModel):
    content = models.TextField()

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