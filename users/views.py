# from tokenize import TokenError
# from django.shortcuts import render
# from jwt import InvalidTokenError
# from django.db.utils import IntegrityError
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.exceptions import ParseError
# from users.serializers import UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer, UserUpdateSerializer, UserDetailSerializer
from users.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenVerifyView

class UserView(APIView):
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class Users(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                # Check for password requirements
                validate_password(serializer.validated_data.get("password"))

                user = serializer.save()
                user.set_password(serializer.validated_data.get("password"))
                user.save()

                return Response(
                    {"success": True, "code": 201, "message": "회원가입 성공"},
                    status=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                errors = []
                for field, messages in e.detail.items():
                    errors.append(
                        {
                            "field": field,
                            "message": messages[
                                0
                            ],  # Assuming there's at least one message per field
                        }
                    )
                return Response(
                    {
                        "error": {
                            "code": 403,
                            "message": _("입력값을 확인해주세요."),
                            "fields": errors,
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "error": {
                        "code": 401,
                        "message": _("유효하지 않은 데이터."),
                        "details": serializer.errors,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = get_object_or_404(User, username=request.user.username)
        # Check if the request user is the same as the user to be updated or if the user is an admin
        if request.user != user and not request.user.is_superuser:
            return Response(
                {"error": {"code": 403, "message": "해당 작업을 수행할 권한 부족"}},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "code": 200, "message": "개인정보 수정 성공"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": "잘못된 요청 형식",
                        "details": serializer.errors,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)

            # 액세스 토큰과 함께 리프레쉬 토큰을 쿠키에 설정
            response = Response({
                'accessToken': str(refresh.access_token),
                'refreshToken': str(refresh),
            })
            response.set_cookie(
                key='access_token', 
                value=str(refresh.access_token), 
                httponly=True, 
                secure=True, 
                samesite='None'
            )
            response.set_cookie(
                key='refresh_token', 
                value=str(refresh), 
                httponly=True, 
                secure=True, 
                samesite='None'
            )

            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class UserDetailView(APIView):
    def get(self, request):
        try:
            user = request.user
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TypeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from datetime import timedelta
# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             access_token = request.headers.get("Authorization").split(" ")[1]
#             token = AccessToken(access_token)
#             token.set_exp(lifetime=timedelta(minutes=0))

#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(
#                 {"success": "Logged out"}, status=status.HTTP_205_RESET_CONTENT
#             )
#         except Exception as e:
#             print(e)
#             return Response(
#                 {
#                     "error": "Refresh token 만료 돼었거나, 없습니다. :",
#                     "example": {"refresh": "your_refresh_token_here"},
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

from rest_framework_simplejwt.exceptions import TokenError
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Attempt to blacklist the provided refresh token
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError as e:
                return Response(
                    {"error": "Token is invalid or expired and cannot be blacklisted."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({"success": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            # Generic exception catch: ideally should be more specific.
            return Response(
                {
                    "error": "An error occurred during logout.",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        # 상위 클래스의 post 메소드를 호출하여 토큰 검증을 수행
        response = super().post(request, *args, **kwargs)

        # 토큰이 유효한 경우, 응답 데이터를 '성공'으로 설정
        if response.status_code == 200:
            response.data = {"message": "성공"}

        return response
