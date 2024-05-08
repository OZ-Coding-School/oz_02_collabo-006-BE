from django.urls import path
from users.views import UserView, Users, UserUpdateAPIView, LoginAPIView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('create/', Users.as_view(), name='user-create'),
    path('<int:user_id>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    # path('logout/', LogoutAPIView.as_view(), name='user-logout'),
    path('login/sjwt/info/', UserDetailView.as_view(), name='user_info'),
    path('login/sjwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/sjwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/sjwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

