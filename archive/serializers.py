from rest_framework import serializers
from archive.models import Archive, ArchiveStatus

class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'

class ArchiveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveStatus
        fields = '__all__'
