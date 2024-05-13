from django.db import models
from common.models import CommonModel
from posts.models import Post

class Media(CommonModel):
    file_url = models.URLField()

    # Post:Media => 1:N
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
