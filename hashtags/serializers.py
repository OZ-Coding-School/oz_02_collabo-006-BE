from rest_framework.serializers import ModelSerializer
from .models import Hashtag

class HashtagSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'