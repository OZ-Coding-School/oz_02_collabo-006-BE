from django.urls import path
from follow.views import FollowerDetail, FollowingDetail, FollowCheckout

urlpatterns = [
    path('follower/', FollowerDetail.as_view(), name='follower-detail'),
    path('following/', FollowingDetail.as_view(), name='following-detail'),
    path('follow/', FollowCheckout.as_view(), name='follow'),
    path('follow/<int:user_id>/', FollowCheckout.as_view(), name='follow-get'),
]