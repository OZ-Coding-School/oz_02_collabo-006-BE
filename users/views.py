from django.urls import reverse
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
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenVerifyView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
import hmac, hashlib, base64, time, requests

def make_signature(method, uri, access_key, secret_key):
    timestamp = str(int(time.time() * 1000))
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    signing_key = bytes(secret_key, 'utf-8')
    message = bytes(message, 'utf-8')
    
    signature = base64.b64encode(hmac.new(signing_key, message, digestmod=hashlib.sha256).digest())
    return signature, timestamp


def send_verification_email(user, verification_link):
    endpoint = settings.CLOUD_OUTBOUND_MAILER_ENDPOINT
    access_key = settings.CLOUD_OUTBOUND_MAILER_ACCESS_KEY
    secret_key = settings.CLOUD_OUTBOUND_MAILER_SECRET_KEY

    method = 'POST'
    uri = '/api/v1/mails'
    
    signature, timestamp = make_signature(method, uri, access_key, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signature.decode('utf-8'),
    }

    payload = {
        "senderAddress": "no_reply@naildp.com",
        "title": "Verify your email address",
        "body": f"{user.username}님 안녕하세요,\n\n이메일 인증하시려면 다음 링크를 클릭해주세요:\n\n\n\n{verification_link}\n\n\n\n감사합니다.!",
        "recipients": [{"address": user.email, "name": user.username, "type": "R"}],
        "individual": True,
        "advertising": False
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.email_verified)

account_activation_token = EmailVerificationTokenGenerator()


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return HttpResponse('Email verification successful')
    else:
        return HttpResponse('Email verification failed')

class Users(APIView):
    def post(self, request, *args, **kwargs):
        account_activation_token = EmailVerificationTokenGenerator()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                # Check for password requirements
                validate_password(serializer.validated_data.get("password"))

                user = serializer.save()
                user.set_password(serializer.validated_data.get("password"))
                user.save()

                # Generate verification link
                token = account_activation_token.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verification_link = request.build_absolute_uri(
                    reverse('email_verification', kwargs={'uidb64': uid, 'token': token})
                )

                # Send verification email
                send_verification_email(user, verification_link)

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


class UserView(APIView):
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


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

# from rest_framework_simplejwt.exceptions import TokenError
class LogoutAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
    # 로그아웃을 위해 현재 사용자의 refresh 토큰 무효화
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                # refresh 토큰을 사용하여 토큰 무효화
                refresh_token = RefreshToken(refresh_token)
                refresh_token.blacklist()

                # 클라이언트에게 쿠키 삭제 요청
                response = Response({'message': 'Successfully logged out'})
                response.delete_cookie('access_token')
                response.delete_cookie('refresh_token')
                response.data = {"success": True}
                return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        # 상위 클래스의 post 메소드를 호출하여 토큰 검증을 수행
        response = super().post(request, *args, **kwargs)

        # 토큰이 유효한 경우, 응답 데이터를 '성공'으로 설정
        if response.status_code == 200:
            response.data = {"message": "성공"}

        return response
