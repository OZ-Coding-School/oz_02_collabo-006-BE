from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Like
from users.models import User
from medias.models import Media
from .serializers import (
    PostListSerializer, 
    PostDetailSerializer, 
    PostCreateSerializer,
    LikeSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
import boto3
import uuid
import base64
from django.core.files.base import ContentFile
# from io import BytesIO

import configparser
CONF = configparser.ConfigParser()
CONF.read('config.ini')


# 전체 게시글 조회
class PostList(APIView):
    permission_classes = [AllowAny] # 인증여부 상관없이 허용

    def get(self, request):
        try:
            # 정렬을 위해 'sort' 매개변수 값 가져오기
            sort = request.GET.get('sort','new')
            # 디폴트 페이지값 : '1' -> 정수형으로 변환
            page = int(request.GET.get('page', '1'))
            page_size = 12  # 페이지당 게시글 수

            # 만약 'sort'가 'new'일 경우
            if sort == 'new':
                # visible(게시글 공개 여부)이 True인 post를 최신순으로 24개씩 가져오기
                posts = Post.objects.filter(visible=True).order_by('-created_at')[:24]
            # 만약 'sort'가 'trending'일 경우
            elif sort == 'trending':
                # visible(게시글 공개 여부)이 True인 post를 좋아요순으로 24개씩 가져오기
                posts = Post.objects.filter(visible=True).order_by('-likes')[:24]
            else:
                return Response({
                    "error": {
                        "code": 400,
                        "message": "유효하지 않은 정렬 매개변수"
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            paginator = Paginator(posts, page_size)
            page_obj = paginator.get_page(page) # 요청된 페이지 번호에 해당하는 게시글 가져오기
            serializer = PostListSerializer(page_obj, many=True) # 페이지에 해당하는 게시글 시리얼라이즈
            
            return Response({
                "success": True,
                "code": 200,
                "message": "전체 게시글 조회 성공",
                "data": serializer.data,
                "current_page": page_obj.number, # 현재 페이지
                "total_pages": paginator.num_pages # 총 페이지
            }, status=status.HTTP_200_OK)

        except Exception as e: # 기타 예외 발생
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
from rest_framework_simplejwt.authentication import JWTAuthentication

class PostCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        media_list = image_upload(request)
        serializer = PostCreateSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                post = serializer.save(user=request.user) # 유저 정보 담기

                if media_list:
                    for media_url in media_list:
                        Media.objects.create(file_url=media_url, post=Post.objects.get(id=post.id))

                return Response({
                    "success": True,
                    "code": 201,
                    "id": post.id,
                    "content": post.content,
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
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 특정 게시글 상세 조회
class PostDetail(APIView):
    permission_classes = [IsAuthenticated] # 인증된 요청(로그인)에 한해 허용

    def get(self, request, post_id):
        try:
            post_obj = Post.objects.get(pk=post_id)

            # visible이 False일 때 현재 사용자가 해당 게시글의 작성자가 아닌 경우, 게시글 조회 불가능
            if not post_obj.visible and post_obj.user != request.user:
                return Response({
                    "error": {
                        "code": 403,
                        "message": "해당 게시글은 비공개 상태입니다."
                    }
                }, status=status.HTTP_403_FORBIDDEN)
            
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

            serializer = PostCreateSerializer(post_obj, data=request.data)

            if serializer.is_valid(raise_exception=True):
                post = serializer.save()
                media_list = image_upload(request)

                # 미디어 수정
                if media_list:
                    for media_url in media_list:
                        # 미디어가 리스트에 없으면 생성 (수정 시 이미지 추가)
                        media, created = Media.objects.get_or_create(file_url=media_url)
                        post.media_set.add(media)

                    for media in post.media_set.all():
                        # DB에 파일이 리스트에 없으면 재거 (수정 시 이미지 제거)
                        if media.file_url not in media_list:
                            post.media_set.remove(media)

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

            if post_obj.user == request.user:
                image_delete(post_id)
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


# 게시글 좋아요     
class PostLike(APIView):
    permission_classes = [IsAuthenticated]

    # 좋아요 개별 조회/리스트조회
    def get(self, request):
        try:
            get_status = request.data.get("get_status")
            # get_status가 True
            if get_status == "True":
                post_id = request.data.get("post_id")
                # 현재 사용자와 게시글에 대한 좋아요 가져오기
                like = Like.objects.filter(user=request.user, post_id=post_id)
                if not like:
                    return Response({"message":"unlike"}, status=200)

                return Response({"post_id": like[0].post.id}, status=status.HTTP_200_OK)
            # get_status가 Fasle일 경우, 리스트 조회
            else:
                post_likes = Like.objects.filter(user=request.user)
                serializer = LikeSerializer(post_likes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 좋아요 생성 및 취소
    def post(self, request):
        try:
            post_id = request.data.get("post_id")
            post_id = Post.objects.get(id=post_id)
            user_obj = User.objects.get(username=request.user)
            existing_like = Like.objects.filter(user=user_obj, post=post_id)
            # 현재 좋아요가 되어있을 때, 좋아요 하면 취소
            if existing_like.exists():
                existing_like.delete()
                post_id.likes -= 1
                post_id.save()
                return Response({"message": "좋아요 취소"}, status=status.HTTP_200_OK)
            # 현재 좋아요가 안 되어있을 때, 좋아요 생성
            else:
                like = Like.objects.create(user=user_obj, post=post_id)
                like.save()
                post_id.likes += 1
                post_id.save()
                return Response({"message": "좋아요 생성"},status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생 : " + str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def image_upload(request):
    # Base64로 인코딩된 이미지 데이터 리스트 추출
    base64_strings = request.data.get('media')
    if not base64_strings:
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

    for base64_string in base64_strings:
        format, imgstr = base64_string.split(';base64,')
        ext = format.split('/')[-1]

        # Base64 문자열을 바이너리 이미지로 디코딩
        data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

        object_name = f"images/{uuid.uuid4()}.{ext}"
        temp_file_path = default_storage.save(object_name, data)

        try:
            # 파일을 S3에 업로드
            s3.upload_file(
                temp_file_path, bucket_name, object_name,
                ExtraArgs={'ACL': 'public-read'}
            )
            public_url = f"{endpoint_url}/{bucket_name}/{object_name}"
            uploaded_files.append(public_url)
            # uploaded_files.append({"file_name": object_name, "url": public_url})
        finally:
            # 임시 파일 삭제
            default_storage.delete(temp_file_path)

    print(uploaded_files)
    return uploaded_files


# 이미지 삭제
def image_delete(post_id):
    # S3 Configuration
    service_name = 's3'
    endpoint_url = 'https://kr.object.ncloudstorage.com/'
    access_key = CONF['ncp']['access']
    secret_key = CONF['ncp']['secret']
    bucket_name = 'oz-nediple'

    # boto3 클라이언트 설정
    s3 = boto3.client(
        service_name, endpoint_url=endpoint_url,
        aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )

    media_objects = Media.objects.filter(post_id=post_id)
    for media_url in media_objects:
        delete_object = str(media_url.file_url).split('https://kr.object.ncloudstorage.com/oz-nediple/')[1]
        s3.delete_object(Bucket=bucket_name, Key=delete_object)
    # response = s3.list_objects(Bucket=bucket_name, MaxKeys=300)

    return