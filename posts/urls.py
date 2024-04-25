from django.urls import path
from .views import (
    PostList, 
    PostCreate, 
    PostDetail, 
    PostUpdate, 
    PostDelete
    )

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('create', PostCreate.as_view(), name='post-create'),
    path('<int:post_id>', PostDetail.as_view(), name='post-detail'),
    path('<int:post_id>/update', PostUpdate.as_view(), name='post-update'),
    path('<int:post_id>/delete', PostDelete.as_view(), name='post-delete'),
]