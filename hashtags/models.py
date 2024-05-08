from django.db import models
from common.models import CommonModel

class Hashtag(CommonModel):
    content = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hashtags'

    def __str__(self):
        return self.content