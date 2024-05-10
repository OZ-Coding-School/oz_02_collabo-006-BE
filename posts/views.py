from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from users.models import User
from .serializers import PostListSerializer, PostDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
import boto3
import uuid
import configparser
CONF = configparser.ConfigParser()
CONF.read('config.ini')


# 전체 게시글 조회
# 게시글 공개 여부가 True인 것만 공개 + 24씩 보내주기
class PostList(APIView):
    permission_classes = [AllowAny] # 인증여부 상관없이 허용

    def get(self, request):
        try:
            posts = Post.objects.filter(visible=True).order_by('-created_at')[:24]

            # 페이징
            page = request.GET.get('page', '1') # 디폴트 페이지값 : '1'
            paginator = Paginator(posts, 12) # 페이지당 12개씩 보여주기S
            page_obj = paginator.get_page(page) # 페이지 번호에 해당하는 게시글 가져오기

            serializer = PostListSerializer(page_obj, many=True)

            return Response({
                "success": True,
                "code": 200,
                "message": "전체 게시글 조회 성공",
                "data": serializer.data,
                "current_page": page_obj.number, # 현재 페이지
                "total_pages": paginator.num_pages # 총 페이지
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 특정 유저의 게시물 리스트 조회
class PostUser(APIView):
    def get(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            posts = Post.objects.filter(user=user, visible=True)

            # 페이징
            page = request.GET.get('page', '1')
            paginator = Paginator(posts, 12)
            page_obj = paginator.get_page(page)
            serializer = PostListSerializer(page_obj, many=True)

            return Response({
                "success": True,
                "code": 200,
                "message": f"USER_ID가 {user_id}인 사용자의 게시글 조회 성공",
                "data": serializer.data,
                "current_page": page_obj.number, # 현재 페이지
                "total_pages": paginator.num_pages # 총 페이지
            })
        
        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 게시글 생성
class PostCreate(APIView):
    permission_classes = [IsAuthenticated] # 인증된 요청(로그인)에 한해 허용

    def post(self, request):
        image_upload(request)
        user_data = request.data
        serializer = PostListSerializer(data=user_data) # 직렬화

        try:
            if serializer.is_valid(raise_exception=True): # 직렬화 데이터가 유효하면
                serializer.save(user=request.user) # 데이터 저장하기 / request.user : 현재 로그인한 사용자
                
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
            print(e)
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 특정 게시글 상세 조회
class PostDetail(APIView):
    permission_classes = [IsAuthenticated] # 인증된 요청(로그인)에 한해 허용

    def get(self, request, post_id):
        try:
            post_obj = Post.objects.get(pk=post_id)
            serializer = PostDetailSerializer(post_obj)
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
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 게시글 수정
class PostUpdate(APIView):
    def post(self, request, post_id):
        try:
            post_obj = Post.objects.get(pk=post_id)

            # 게시글 작성자와 현재 유저가 같지 않으면 수정 권한이 없다.
            if post_obj.user != request.user:
                return Response({
                    "error": {
                        "code": 403,
                        "message": "해당 작업을 수행할 권한이 없습니다."
                    }
                }, status=status.HTTP_403_FORBIDDEN)
            
            user_data = request.data
            serializer = PostDetailSerializer(post_obj, data=user_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
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
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 게시물 삭제
class PostDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post_obj = get_object_or_404(Post, pk=post_id)

            # 게시글 작성자와 현재 유저가 같지 않으면 삭제 권한이 없다.
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
                "message": "게시글 삭제 성공"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




# def image_upload(request):
#     image = request.FILES.get('image')
#     if not image:
#         return Response({"error": "No image provided"}, status=400)

#     # Configure S3 client
#     service_name = 's3'
#     endpoint_url = 'https://kr.object.ncloudstorage.com'
#     access_key = CONF['ncp']['access']
#     secret_key = CONF['ncp']['secret']
#     bucket_name = 'oz-nediple'

#     s3 = boto3.client(
#         service_name, endpoint_url=endpoint_url,
#         aws_access_key_id=access_key, aws_secret_access_key=secret_key
#     )

#     # Create unique file name and save temporarily
#     object_name = f"images/{uuid.uuid4()}-{image.name}"
#     temp_file_path = default_storage.save(object_name, image)

#     try:
#         # Upload file with public read access
#         s3.upload_file(
#             temp_file_path, bucket_name, object_name,
#             ExtraArgs={'ACL': 'public-read'}
#         )
#     finally:
#         # Clean up temporary file
#         default_storage.delete(temp_file_path)

#     public_url = f"{endpoint_url}/{bucket_name}/{object_name}"
#     return public_url


def image_upload(request):
    # 'media' 키로 전송된 모든 이미지 리스트로 가져오기
    images = request.FILES.getlist('media')
    # 이미지가 전송되지 않으면 에러 반환
    if not images:
        return Response({"error": "No images provided"}, status=400)

    # S3 Configuration
    service_name = 's3'
    endpoint_url = 'https://kr.object.ncloudstorage.com'
    access_key = CONF['ncp']['access']
    secret_key = CONF['ncp']['secret']
    bucket_name = 'oz-nediple'

    # boto3 클라이언트 설정
    s3 = boto3.client(
        service_name, endpoint_url=endpoint_url,
        aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )

    # 업로드된 파일 정보 저장
    uploaded_files = []

    for image in images:
        object_name = f"images/{uuid.uuid4()}-{image.name}"
        temp_file_path = default_storage.save(object_name, image)

        try:
            s3.upload_file(
                temp_file_path, bucket_name, object_name,
                ExtraArgs={'ACL': 'public-read'}
            )
            public_url = f"{endpoint_url}/{bucket_name}/{object_name}"
            uploaded_files.append({"file_name": object_name, "url": public_url})
        finally:
            default_storage.delete(temp_file_path)

    print(uploaded_files)
    return uploaded_files



# from medias.models import Media  # Ensure you have the correct import for your models

# def image_upload(request):
#     images = request.FILES.getlist('media')
#     if not images:
#         return Response({"error": "No images provided"}, status=400)

#     # S3 Configuration
#     service_name = 's3'
#     endpoint_url = 'https://kr.object.ncloudstorage.com'
#     access_key = CONF['ncp']['access']
#     secret_key = CONF['ncp']['secret']
#     bucket_name = 'oz-nediple'

#     s3 = boto3.client(
#         service_name, endpoint_url=endpoint_url,
#         aws_access_key_id=access_key, aws_secret_access_key=secret_key
#     )

#     uploaded_files = []

#     for image in images:
#         object_name = f"images/{uuid.uuid4()}-{image.name}"
#         temp_file_path = default_storage.save(object_name, image)

#         try:
#             s3.upload_file(
#                 temp_file_path, bucket_name, object_name,
#                 ExtraArgs={'ACL': 'public-read'}
#             )
#             public_url = f"{endpoint_url}/{bucket_name}/{object_name}"
#             uploaded_files.append({"file_name": object_name, "url": public_url})
            
#             # Save to Media model
#             media = Media(file_url=public_url, post=serializer.instance)
#             media.save()

#         finally:
#             default_storage.delete(temp_file_path)

#     return uploaded_files

class LatestPostsAPI(APIView):
    def get(self, request):
        pagenum = request.data['page']
        latest_posts = Post.objects.all().order_by('-created_at')[(pagenum-1)*24:pagenum*24]
        latest_posts = Post.objects.all().order_by('-created_at')[:24]
        serializer = PostListSerializer(latest_posts, many=True)
        return Response(serializer.data)