from datetime import timedelta
from pathlib import Path
import platform

import configparser

CONF = configparser.ConfigParser()
CONF.read("config.ini")


# 개발환경과 서버환경 구분을 위한 변수
platform_index = platform.system()
# Linux

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-kjvg#186o8lgqv8_6t0e^su@%mpjy5_-a#ur6x&@&5k*%^%%rx"

# SECURITY WARNING: don't run with debug turned on in production!

if platform_index == "Linux":
    DEBUG = False
else:
    DEBUG = True


ALLOWED_HOSTS = ["*"]


CORS_ORIGIN_ALLOW_ALL = True

# CSRF_TRUSTED_ORIGINS = ["*"]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
]


# CORS_ALLOWED_ORIGINS = [
#     "http://223.130.133.22/",  # 클라이언트 애플리케이션의 출처(origin)에 따라 수정
# ]

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

# Application definition

DJANGO_SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CUSTOM_USER_APPS = [
    "searching.apps.SearchingConfig",
    "users.apps.UsersConfig",
    "common.apps.CommonConfig",
    "posts.apps.PostsConfig",
    "medias.apps.MediasConfig",
    "comments.apps.CommentsConfig",
    "hashtags.apps.HashtagsConfig",
    "follow.apps.FollowConfig",
    "archive.apps.ArchiveConfig",
    "search.apps.SearchConfig",
]

CUSTOM_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_yasg",
    "rest_framework_simplejwt.token_blacklist",
]


INSTALLED_APPS = DJANGO_SYSTEM_APPS + CUSTOM_USER_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# 서버에 올렸을때와 로컬완경에서 개발할때의 db 선택
if platform_index == "Linux":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "db",
            "USER": "admin",
            "PASSWORD": "admin",
            "HOST": "db",
            "PORT": "5432",  # 5432는 PostgreSQL의 기본포트이다
        }
    }
else:
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.mysql",
    #         "NAME": CONF["mysql"]["DB_NAME"],
    #         "USER": CONF["mysql"]["DB_USER"],
    #         "PASSWORD": CONF["mysql"]["DB_PASS"],
    #         "HOST": CONF["mysql"]["BD_HOST"],
    #         "PORT": CONF["mysql"]["BD_PORT"],
    #     }
    # }
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


AUTH_USER_MODEL = "users.User"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

if platform_index == "Linux":
    STATIC_URL = "/static/"
    STATICFILES_DIRS = []
else:
    STATIC_URL = "/static/"
    STATICFILES_DIRS = []


STATIC_ROOT = "/static/"
# STATIC_ROOT = BASE_DIR / 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        # 'rest_framework.authentication.SessionAuthentication',
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


SIMPLE_JWT = {
    # 액세스 토큰의 유효 기간을 5분으로 설정합니다.
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=600),
    # 리프레시 토큰의 유효 기간을 1일로 설정합니다.
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # 리프레시 토큰을 갱신할 때마다 새 토큰을 생성하지 않도록 설정합니다.
    "ROTATE_REFRESH_TOKENS": False,
    # 토큰을 갱신한 후 이전 토큰을 블랙리스트에 추가합니다.
    "BLACKLIST_AFTER_ROTATION": True,
    # JWT에 사용할 서명 알고리즘으로 HS256을 사용합니다.
    "ALGORITHM": "HS256",
    # JWT를 서명하는 데 사용할 키로 Django의 SECRET_KEY를 사용합니다.
    "SIGNING_KEY": SECRET_KEY,
    # JWT 검증에 사용할 키입니다. HS256 알고리즘에서는 None으로 설정됩니다.
    "VERIFYING_KEY": None,
    # 인증 헤더의 타입으로 'Bearer'를 사용합니다.
    # Authorization: Bearer <token>
    "AUTH_HEADER_TYPES": ("Bearer",),
    # 토큰에 포함될 사용자 식별자 필드로 'id'를 사용합니다.
    "USER_ID_FIELD": "id",
    # 토큰 클레임에서 사용자 식별자에 해당하는 키로 'user_id'를 사용합니다.
    "USER_ID_CLAIM": "user_id",
    # 사용할 토큰 클래스로 AccessToken을 사용합니다.
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/path/to/django/logs/debug.log',  # 로그 파일 경로 수정 필요
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


CORS_ORIGIN_WHITELIST = []

CORS_ALLOW_CREDENTIALS = True



CLOUD_OUTBOUND_MAILER_ENDPOINT = 'https://mail.apigw.ntruss.com/api/v1/mails'
CLOUD_OUTBOUND_MAILER_ACCESS_KEY = CONF["ncp"]["access"]
CLOUD_OUTBOUND_MAILER_SECRET_KEY = CONF["ncp"]["secret"]