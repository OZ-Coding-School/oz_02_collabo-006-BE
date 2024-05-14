from django.shortcuts import render
from follow.models import Follower, Following
from follow.serializers import FollowerSerializer, FollowingSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class FollwerCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FollowerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




# 팔로워 조회
# user = User.objects.get(id=1)
# followers = user.follower_from.all()

# 팔로잉 조회
# user = User.objects.get(id=1)
# following = user.follower_to.all()

# 팔로잉 관계 조회
# user = User.objects.get(id=1)
# followings = user.following_from.all()

# 나를 팔로우하는 사용자 조회
# user = User.objects.get(id=1)
# followers_of = user.following_to.all()
