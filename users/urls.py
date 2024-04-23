from django.urls import path
from users.views import UserView, Users, UserUpdateAPIView, LoginAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('', Users.as_view()),
    path('<int:user_id>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('sjwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sjwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("sjwt/verify/", TokenVerifyView.as_view(), name='token_verify'),
]

