from django.urls import path
from users.views import Users, UserUpdateAPIView, UserDetailView, LogoutAPIView, CustomTokenVerifyView, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView
# from users.views import UserView
# from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView


urlpatterns = [
    path('create/', Users.as_view(), name='user-create'),
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('logout/', LogoutAPIView.as_view(), name='user-logout'),
    path('info/', UserDetailView.as_view(), name='user_info'),
    path('jwt/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login/', LoginAPIView.as_view(), name='user-login'),
    # path('login/sjwt/info/', UserDetailView.as_view(), name='user_info'),
    # path('login/sjwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/sjwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login/sjwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

