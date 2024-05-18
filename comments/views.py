from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from posts.models import Post
from .serializers import CommentCreateSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator

# 게시글 내 댓글 생성
class CommentCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:            
            post = Post.objects.get(id=post_id)

            # 해당 게시물이 존재하지 않으면 에러 발생
            if not post:
                return Response({'message': '해당 게시글이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            # 게시물이 댓글 작성을 허용하지 않는 경우 에러 발생
            if not post.comment_ck:
                return Response({'message': '해당 게시글은 댓글을 작성할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            parent_comment = request.data.get('parent_comment', None)
            content = request.data.get('content', None)
            
            # 'content' 필드가 없으면 에러 발생
            if not content:
                return Response({'message': '댓글 내용을 입력해 주세요.'}, status=status.HTTP_400_BAD_REQUEST)

            # 부모 댓글이 지정되어 있고 해당 부모 댓글이 존재하지 않는 경우 에러 발생
            if parent_comment and not Comment.objects.filter(id=parent_comment).exists():
                return Response({'message': '해당 부모 댓글을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = CommentCreateSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, post=post)

                return Response({
                    "success": True,
                    "code": 201,
                    "message": "댓글 생성 성공",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 게시글 내 댓글 조회
class CommentRead(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        pass

# 게시글 내 댓글 수정
class CommentUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, comment_id):
        pass

# 게시글 내 댓글 삭제
class CommentDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        pass