from django.shortcuts import get_object_or_404, render
from follow.models import Follower, Following
from follow.serializers import FollowerSerializer, FollowingSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class FollowerCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = FollowerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FollowerDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            follower_obj = get_object_or_404(Follower, pk=user_id)
            serializer = FollowerSerializer(follower_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Follower.DoesNotExist:
            return Response({'error': 'Follower does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class FollowerDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            follower_obj = get_object_or_404(Follower, pk=request.data['user_id'])
            follower_obj.delete()
            return Response({'message': 'Follower deleted'}, status=status.HTTP_200_OK)
        except Follower.DoesNotExist:
            return Response({'error': 'Follower does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowingCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = FollowingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FollowingDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            following_obj = get_object_or_404(Following, pk=user_id)
            serializer = FollowingSerializer(following_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Following.DoesNotExist:
            return Response({'error': 'Following does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FollowingDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            following_obj = get_object_or_404(Following, pk=request.data['user_id'])
            following_obj.delete()
            return Response({'message': 'Following deleted'}, status=status.HTTP_200_OK)
        except Following.DoesNotExist:
            return Response({'error': 'Following does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
