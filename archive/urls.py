
from django.urls import path
from .views import *

urlpatterns = [
    path('', ArchiveListCreateAPIView.as_view(), name='archive-list-create'),
    path('delete/', ArchiveListDelete.as_view(), name='archive-delete'),
    path('update/', ArchiveListUpdate.as_view(), name='archive-update'),
    path('<int:pk>/', ArchiveDetailAPIView.as_view(), name='archive-detail'),
    path('<int:archive_pk>/add_post/', ArchivePostCreateAPIView.as_view(), name='archive-add-post'),
    path('<int:archive_pk>/delete_post/', ArchivePostDeleteAPIView.as_view(), name='archive-delete-post'),
]

# ArchiveListCreateAPIView: 아카이브 목록을 가져오고 새로운 아카이브를 생성합니다.
# ArchiveDetailAPIView: 특정 아카이브를 가져오고 삭제합니다.
# ArchivePostCreateAPIView: 특정 아카이브에 게시물을 추가합니다.