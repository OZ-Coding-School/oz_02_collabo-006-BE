from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer, PostDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator

# 전체 게시글 조회
class PostList(APIView):
    def get(self, request):
        try:
            posts = Post.objects.order_by('-created_at')

            # 페이징
            page = request.GET.get('page', '1') # 디폴트 페이지값 : '1'
            paginator = Paginator(posts, 12) # 페이지당 12개씩 보여주기
            page_obj = paginator.get_page(page) # 페이지 번호에 해당하는 게시글 가져오기

            serializer = PostSerializer(page_obj, many=True)

            return Response({
                "success": True,
                "code": 200,
                "message": "전체 게시글 조회 성공",
                "data": serializer.data,
                "current_page": page_obj.number, # 현재 페이지
                "total_pages": paginator.num_pages # 총 페이지
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # print(e)
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생"
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 게시글 생성
class PostCreate(APIView):
    # permission_classes = [IsAuthenticated]

    from hashtags.views import HashtagCreate

    def post(self, request):
        user_data = request.data
        serializer = PostSerializer(data=user_data)

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                
                return Response({
                    "success": True,
                    "code": 201,
                    "message": "게시글 생성 성공",
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
                    "message": "서버 내 오류 발생"
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 특정 게시글 조회
class PostDetail(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            serializer = PostDetailSerializer(post)
            return Response({
                "success": True,
                "code": 200,
                "message": "하나의 게시글 조회 성공",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({
                "error": {
                    "code": 404,
                    "message": "해당 ID의 게시글이 존재하지 않음"
                }
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생"
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 게시글 수정
class PostUpdate(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post_obj = Post.objects.get(pk=post_id)
            user_data = request.data
            serializer = PostDetailSerializer(post_obj, data=user_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save() # 사용자 기록
                return Response({
                    "success": True,
                    "code": 200,
                    "message": "게시글 수정 성공",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            
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
                    "message": "서버 내 오류 발생"
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 게시물 삭제
class PostDelete(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post_obj = get_object_or_404(Post, pk=post_id)

            if post_obj.user != request.user:
                return Response({
                    "error": {
                        "code": 403,
                        "message": "해당 작업을 수행할 권한이 없습니다."
                    }
                }, status=status.HTTP_403_FORBIDDEN)

            post_obj.delete()

            return Response({
                "success": True,
                "code": 200,
                "message": "게시글 수정 성공"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생"
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)