from django.db import models
from common.models import CommonModel
from users.models import User
from hashtags.models import Hashtag
# from medias.models import Media

class Post(CommonModel):
    content = models.TextField(blank=True)
    comment_ck = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)

    # User:Post => 1:N
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Hashtag:Post => N:M
    hashtag = models.ManyToManyField(Hashtag, through='HashtagPost', blank=True)
    # Media:Post => N:M
    # media = models.ForeignKey(Media)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HashtagPost(CommonModel):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hashtag_post'