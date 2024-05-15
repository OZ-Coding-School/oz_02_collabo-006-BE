from django.urls import path
from follow.views import FollowerCreate, FollowerDetail, FollowerDelete, FollowingCreate, FollowingDelete, FollowingDetail, FollowingDelete

urlpatterns = [
    path('follower/create/', FollowerCreate.as_view(), name='follower-create'),
    path('follower/<int:user_id>/', FollowerDetail.as_view(), name='follower-detail'),
    path('follower/delete/', FollowerDelete.as_view(), name='follower-delete'),
    path('following/create/', FollowingCreate.as_view(), name='following-create'),
    path('following/<int:user_id>/', FollowingCreate.as_view(), name='following-detail'),
    path('following/delete/', FollowingDelete.as_view(), name='following-delete'),
]