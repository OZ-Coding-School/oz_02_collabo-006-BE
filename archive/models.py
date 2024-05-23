# archive/models.py
from django.db import models
from users.models import User
from common.models import CommonModel
from posts.models import Post

class ArchiveStatus(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='archive_status')
    current_archive_count = models.IntegerField(default=0)
    max_archive_count = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.user.username} status"

class Archive(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archives')
    archive_name = models.CharField(max_length=8)
    description = models.TextField(default="")
    status = models.ForeignKey(ArchiveStatus, on_delete=models.CASCADE, related_name='archives')

    def __str__(self):
        return self.archive_name

class ArchivePost(CommonModel):
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, related_name='archive_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='archive_posts')

class Meta:
    unique_together = ('archive', 'post')
    verbose_name = 'Archive Post'
    verbose_name_plural = 'Archive Posts'

    def __str__(self):
        return f"Archive: {self.archive.archive_name}, Post: {self.post.id}"

