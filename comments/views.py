from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from users.models import User
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator

# 게시글 내 댓글 생성
class CommentCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post_obj = get_object_or_404(Post, pk=post_id)

        if not post_obj.comment_ck:
            return Response({
                "error": {
                    "code": 403,
                    "message": "해당 게시글은 댓글을 작성할 수 없습니다."
                }
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentSerializer(data=request.data)
        
        try:
            if serializer.is_valid(raise_exception=True):
                comment = serializer.save(user=request.user)

                return Response({
                    "success": True,
                    "code": 201,
                    "message": "댓글 생성 성공",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            errors = []
            for field, messages in e.detail.items():
                errors.append({
                    "field": field,
                    "message": messages[0]
                })

            return Response({
                "error": {
                    "code": 400,
                    "message": _("입력값을 확인해주세요."),
                    "fields": errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
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