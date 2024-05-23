from django.db import models
from common.models import CommonModel
from users.models import User

class Follower(CommonModel):
    user = models.ForeignKey(User, related_name='follower_from', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower_to', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.follower} follows {self.user}"

class Following(CommonModel):
    user = models.ForeignKey(User, related_name='following_from', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following_to', on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user', 'following')

    def __str__(self):
        return f"{self.user} follows {self.following}"
