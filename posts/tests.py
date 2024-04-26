from rest_framework.test import APITestCase
from users.models import User
from .models import Post
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import pdb

class PostAPITestCase(APITestCase):
    # (1) 유저 생성/로그인 -> (2) 게시글 생성
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'nail_dp',
            phone = '01012345678',
            password = 'nailpassword123'
        )

        self.client.login(username='nail_dp', password='nailpassword123')

        self.post = Post.objects.create(
            content = '내가 제일 좋아하는 네일',
            comment_ck = True,
            visible = False,
            user = self.user
        )

    # 전체 게시글 조회
    def test_post_list_get(self):
        url = reverse('post-list')

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        self.assertTrue(len(res.data) > 0)

    # 게시글 생성
    def test_post_create_post(self):
        url = reverse('post-create')

        data = {
            'content': 'test post',
            'media': ['2', '1'],
            'hashtag': ['파인애플', '사과'],
            'comment_ck': 'True',
            'visible': 'True',
            'user': self.user.pk
        }

        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['content'], 'test post')

    # 특정 게시글 조회
    def test_post_detail_get(self):
        url = reverse('post-detail', kwargs={'pk':self.post.pk})

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # 특정 게시글 업데이트
    def test_post_update_post(self):
        url = reverse('video-update', kwargs={'pk':self.post.pk})

        data = {
            'content': 'update test post',
            'media': ['2', '1'],
            'hashtag': ['파인애플', '사과'],
            'comment_ck': 'True',
            'visible': 'True',
            'user': self.user.pk
        }

        res = self.client.put(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['content'], 'update test post')

    # 특정 게시글 삭제
    def test_post_delete_post(self):
        url = reverse('video-delete', kwargs={'pk':self.post.pk})

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)