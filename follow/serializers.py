from rest_framework.serializers import ModelSerializer
from follow.models import Follower, Following

class FollowerSerializer(ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'

class FollowingSerializer(ModelSerializer):
    class Meta:
        model = Following
        fields = '__all__'
