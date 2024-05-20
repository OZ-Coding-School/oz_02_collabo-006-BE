from django.urls import path
from .views import (
    PostList, 
    PostUser,
    PostCreate, 
    PostDetail, 
    PostUpdate, 
    PostDelete,
    PostLikeView
    )

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('user/<int:user_id>/', PostUser.as_view(), name='post-user'),
    path('create/', PostCreate.as_view(), name='post-create'),
    path('<int:post_id>/', PostDetail.as_view(), name='post-detail'),
    path('<int:post_id>/update/', PostUpdate.as_view(), name='post-update'),
    path('<int:post_id>/delete/', PostDelete.as_view(), name='post-delete'),
    path('like/', PostLikeView.as_view(), name='post-like'),
]