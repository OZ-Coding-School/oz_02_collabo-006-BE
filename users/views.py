from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer, UserUpdateSerializer, UserLoginSerializer
from users.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



class UserView(APIView):
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

# post 유저생성
@method_decorator(csrf_exempt, name='dispatch')
class Users(APIView):
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
            print(e.message)
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



class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        # Check if the request user is the same as the user to be updated or if the user is an admin
        if request.user != user and not request.user.is_superuser:
            return Response({
                "error": {
                    "code": 403,
                    "message": "해당 작업을 수행할 권한 부족"
                }
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "code": 200,
                "message": "개인정보 수정 성공"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": {
                    "code": 400,
                    "message": "잘못된 요청 형식",
                    "details": serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)




class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Here, handle creating/authenticating a token or session for the user
            return Response({
                "success": True,
                "code": 200,
                "message": "로그인 성공",
                # Optionally include additional user data or a token here
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
