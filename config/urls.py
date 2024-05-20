from django.contrib import admin
from django.urls import path, include

# swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg       import openapi
from django.conf import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('users.urls')),
    path('api/v1/post/', include('posts.urls')),
    path('api/v1/comment/', include('comments.urls')),
    path('api/v1/', include('follow.urls')),
    path('api/v1/archive/', include('archive.urls')),
    path('api/v1/search/', include('search.urls')),
]

# # swagger
# schema_view = get_schema_view(
#     openapi.Info(
#         title="네디플",
#         default_version='1.1.1',
#         description="네디플 백엔드 API",
#         # terms_of_service="https://www.google.com/policies/terms/",
#         # contact=openapi.Contact(email="이메일"), # 부가정보
#         # license=openapi.License(name="mit"),     # 부가정보
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )

# urlpatterns += [
#     path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
# ]






# import os

# for app in settings.CUSTOM_USER_APPS:
#     app = app.split('.')[0]
#     if not os.path.exists(os.path.join(settings.BASE_DIR, app, 'urls.py')):
#         continue
#     urlpatterns += [
#         path(f'api/v1/{app}/', include(f'{app}.urls')),
#     ]
# urlpatterns += [
#     path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
# ]