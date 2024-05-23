from django.db import models
from common.models import CommonModel
from users.models import User
from hashtags.models import Hashtag

# 게시글 테이블
class Post(CommonModel):
    content = models.TextField(blank=True)
    comment_ck = models.BooleanField(default=True) # 댓글 작성 가능 여부
    visible = models.BooleanField(default=True) # 게시글 조회 가능 여부
    likes = models.PositiveIntegerField(default=0)

    # User:Post => 1:N
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Hashtag:Post => N:M
    hashtag = models.ManyToManyField(Hashtag, through='HashtagPost', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'

# 해시태그-게시글 중간테이블
class HashtagPost(CommonModel):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hashtag_post'

# 게시글 좋아요 테이블
class PostLike(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post')
        ]