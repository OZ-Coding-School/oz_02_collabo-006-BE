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
            
            parent_comment_id = request.data.get('parent_comment', None)
            content = request.data.get('content', None)
            
            # 'content' 필드가 없으면 에러 발생
            if not content:
                return Response({'message': '댓글 내용을 입력해 주세요.'}, status=status.HTTP_400_BAD_REQUEST)

            if parent_comment_id:
                parent_comment = get_object_or_404(Comment, id=parent_comment_id)
                # 부모 댓글이 대댓글인 경우, 즉, 부모 댓글이 이미 다른 댓글의 자식인 경우
                if parent_comment.parent_comment is not None:
                    return Response({'message': '대댓글에는 댓글을 작성할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                parent_comment = None

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
        try:
            post = get_object_or_404(Post, id=post_id)
            comments = Comment.objects.filter(post=post, parent_comment=None).order_by('created_at')
            serializer = CommentSerializer(comments, many=True)

            return Response({
                "success": True,
                "code": 200,
                "message": "댓글 조회 성공",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 게시글 내 댓글 수정
class CommentUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        try:            
            comment = get_object_or_404(Comment, id=comment_id)

            # 현재 사용자와 댓글 작성자가 동일한지 확인
            if comment.user != request.user:
                return Response({
                    "error": {
                        "code": 403,
                        "message": "해당 작업을 수행할 권한이 없습니다."
                    }
                }, status=status.HTTP_403_FORBIDDEN)

            if not comment.post:
                return Response({'message': '해당 게시글이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            content = request.data.get('content', None)

            if not content:
                return Response({'message': '댓글 내용을 입력해 주세요.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 댓글 내용 업데이트
            comment.content = content
            comment.save()

            serializer = CommentSerializer(comment)

            return Response({
                "success": True,
                "code": 201,
                "message": "댓글 수정 성공",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 게시글 내 댓글 삭제
class CommentDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        try:
            comment = get_object_or_404(Comment, pk=comment_id)

            # 게시글 작성자와 현재 유저가 같지 않으면 삭제 권한이 없다.
            if comment.user != request.user:
                return Response({
                    "error": {
                        "code": 403,
                        "message": "해당 작업을 수행할 권한이 없습니다."
                    }
                }, status=status.HTTP_403_FORBIDDEN)

            # 현재 사용자가 댓글 작성자거나 게시글 작성자일 경우 삭제 가능하다.
            if comment.user == request.user or comment.post.user == request.user:
                comment.delete()

                return Response({
                    "success": True,
                    "code": 200,
                    "message": "댓글 삭제 성공"
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)