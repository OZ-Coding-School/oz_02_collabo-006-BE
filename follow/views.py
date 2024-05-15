from django.shortcuts import get_object_or_404, render
from follow.models import Follower, Following
from follow.serializers import FollowerSerializer, FollowingSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User

class FollowCheckout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            target_user_id = request.data.get('user_id')

            if not target_user_id:
                return Response({'error': 'user_id query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            # 팔로우 상태 확인
            is_following = Follower.objects.filter(user=target_user_id, follower=user.id).exists()

            return Response({'is_following': is_following}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            target_user_id = request.data.get('user_id')
            user_status = request.data.get('status')
            if user.id == target_user_id:
                return Response({'message': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

            if user_status is True:
                # 중복 검사: 이미 팔로우 중인지 확인
                if Follower.objects.filter(user=target_user_id, follower=user.id).exists():
                    return Response({'message': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)

                follower_data = {
                    'user': target_user_id,
                    'follower': user.id
                }
                following_data = {
                    'user': user.id,
                    'following': target_user_id
                }

                follower_serializer = FollowerSerializer(data=follower_data)
                follower_serializer.is_valid(raise_exception=True)
                follower_serializer.save()

                following_serializer = FollowingSerializer(data=following_data)
                following_serializer.is_valid(raise_exception=True)
                following_serializer.save()

                return Response({'message': 'Followed successfully'}, status=status.HTTP_201_CREATED)

            elif user_status is False:
                # 중복 검사: 이미 언팔로우 상태인지 확인
                follower_instance = Follower.objects.filter(user=target_user_id, follower=user.id).first()
                following_instance = Following.objects.filter(user=user.id, following=target_user_id).first()

                if not follower_instance or not following_instance:
                    return Response({'message': 'Not following this user'}, status=status.HTTP_400_BAD_REQUEST)

                follower_instance.delete()
                following_instance.delete()

                return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# user = User.objects.get(id=1)
# followers = user.follower_from.all()

class FollowerDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            username = request.data.get('username')
            if username:
                user = get_object_or_404(User, username=username)
            else:
                user = request.user

            followers = Follower.objects.filter(user=user)
            serializer = FollowerSerializer(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': "서버 내 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class FollowingDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            username = request.data.get('username')
            if username:
                user = get_object_or_404(User, username=username)
            else:
                user = request.user

            followings = Following.objects.filter(user=user)
            serializer = FollowingSerializer(followings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


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
