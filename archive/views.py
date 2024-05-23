# archive/views.py
from rest_framework import status as drf_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Archive, ArchiveStatus, ArchivePost
from .serializers import ArchiveSerializer, ArchiveStatusSerializer, ArchivePostSerializer
from django.shortcuts import get_object_or_404
from posts.models import Post

class ArchiveListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        archives = Archive.objects.filter(user=request.user)
        serializer = ArchiveSerializer(archives, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        archive_status, created = ArchiveStatus.objects.get_or_create(user=user)

        if archive_status.current_archive_count >= archive_status.max_archive_count:
            return Response(
                {"error": "아카이브 사용량이 최대치 입니다.."},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['user'] = user.id  # 현재 로그인된 사용자를 user 필드에 할당

        serializer = ArchiveSerializer(data=data)
        if serializer.is_valid():
            archive = serializer.save(user=user, status=archive_status)
            archive_status.current_archive_count += 1
            archive_status.save()
            return Response(serializer.data, status=drf_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

class ArchiveListDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        archive_id = request.data.get('archive_id')
        archive = get_object_or_404(Archive, pk=archive_id, user=request.user)
        archive.delete()

        # Update the current archive count
        archive_status = ArchiveStatus.objects.get(user=request.user)
        archive_status.current_archive_count -= 1
        archive_status.save()

        return Response({'status': 'archive deleted'}, status=drf_status.HTTP_200_OK)

class ArchiveListUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        archive_id = request.data.get('archive_id')
        archive = get_object_or_404(Archive, pk=archive_id, user=request.user)
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ArchiveSerializer(archive, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=drf_status.HTTP_200_OK)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)


class ArchiveDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        archive = get_object_or_404(Archive, pk=pk, user=request.user)
        serializer = ArchiveSerializer(archive)
        return Response(serializer.data)
    
    
class ArchivePostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, archive_pk):
        archive = get_object_or_404(Archive, pk=archive_pk, user=request.user)
        post_id = request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        # Check if the ArchivePost already exists
        if ArchivePost.objects.filter(archive=archive, post=post).exists():
            return Response({'status': 'post already in archive'}, status=drf_status.HTTP_400_BAD_REQUEST)

        ArchivePost.objects.create(archive=archive, post=post)

        return Response({'status': 'post added'}, status=drf_status.HTTP_200_OK)

class ArchivePostDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, archive_pk):
        archive = get_object_or_404(Archive, pk=archive_pk, user=request.user)
        post_id = request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        archive_post = get_object_or_404(ArchivePost, archive=archive, post=post)
        archive_post.delete()
        return Response({'status': 'post deleted'}, status=drf_status.HTTP_200_OK)
    