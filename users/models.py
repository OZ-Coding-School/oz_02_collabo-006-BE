from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # Inheriting default user fields like username, password, email, etc., from AbstractUser

    # Custom fields from your table specification
    phone = models.CharField(max_length=30, null=False, unique=True)      # 휴대폰 번호, Not Null
    email = models.EmailField(unique=True, null=False, default='')
    profile_image = models.TextField(null=True)              # 프로필 이미지 URL, can be null
    referrer = models.CharField(max_length=30, null=True, blank=True)    # 추천인, can be null
    subscription = models.BooleanField(default=False)        # 구독 여부, 기본값 False
    status = models.IntegerField(default=0, null=False)      # 회원 상태 (가입:0, 활동중:1, 탈퇴:2, 휴먼:3), Not Null

    # Additional fields for metadata handling from CommonModel
    created_at = models.DateTimeField(auto_now_add=True)     # 생성시간, 자동 생성
    updated_at = models.DateTimeField(auto_now=True)         # 수정시간, 자동 업데이트

    class Meta:
        db_table = 'users'  # 명시적으로 테이블 이름 지정
