from django.urls import path
from follow.views import FollwerCreate

urlpatterns = [
    path('followers/create/', FollwerCreate.as_view(), name='follower-create'),
]