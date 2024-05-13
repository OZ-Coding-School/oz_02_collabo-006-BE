from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Hashtag

# 해시태그 생성
class HashtagCreate(APIView):
    permission_classes = [IsAuthenticated] # 인증된 요청(로그인)에 한해 허용

    def post(self, request):
        try:
            post_data = request.data

            # 해시태그 ','로 구분
            hashtag_string = post_data.get('content', '')
            # ','를 공백으로 대체
            hashtag_string = hashtag_string.replace(",", "")
            # '#' 제거 후 공백을 기준으로 해시태그 구분
            hashtag_list = hashtag_string.split("#")

            for tag in hashtag_list:
                # 양쪽 공벡 제거
                tag_content = tag.strip()
                if tag_content == "":
                    continue
                hashtag, created = Hashtag.objects.get_or_create(content=tag_content)
                
            return Response({
                "success": True,
                "code": 201,
                "message": "해시태그 생성 성공"
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