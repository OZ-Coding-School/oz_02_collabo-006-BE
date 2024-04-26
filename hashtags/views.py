from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from .serializers import HashtagSerializer

class HashtagCreate(APIView):
    def post(self, request):
        post_data = request.data
        serializer = HashtagSerializer(data=post_data)

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response({
                    "success": True,
                    "code": 201,
                    "message": "해시태그 생성 성공",
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