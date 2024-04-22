from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer, MyInfoUserSerializer
from users.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _



class UserView(APIView):
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    



class Users(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                # Check for password requirements
                validate_password(serializer.validated_data.get('password'))
                
                user = serializer.save()
                user.set_password(serializer.validated_data.get('password'))
                user.save()

                return Response({
                    "success": True,
                    "code": 201,
                    "message": "회원가입 성공"
                }, status=status.HTTP_201_CREATED)
                
        except ValidationError as e:
            errors = []
            for field, messages in e.detail.items():
                errors.append({
                    "field": field,
                    "message": messages[0]  # Assuming there's at least one message per field
                })

            return Response({
                "error": {
                    "code": 400,
                    "message": _("입력값을 확인해주세요."),
                    "fields": errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Generic error handling
            return Response({
                "error": {
                    "code": 500,
                    "message": "서버 내 오류 발생"
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # If all validations pass
        instance = serializer.save()
        return Response({
            "success": True,
            "message": _("회원가입 성공"),
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
