from django.db import models
from users.models import User
from common.models import CommonModel
from posts.models import Post



class Archive(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archives')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='archived_in')
    archive_name = models.CharField(max_length=8)
    description = models.TextField()

    def __str__(self):
        return self.archive_name

class ArchiveStatus(models.Model):
    archive = models.OneToOneField(Archive, on_delete=models.CASCADE, related_name='status')
    current_archive_count = models.IntegerField(default=0)
    max_archive_count = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.archive.archive_name} status"
