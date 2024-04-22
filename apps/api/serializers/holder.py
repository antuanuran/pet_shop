from rest_framework import serializers

from apps.api.serializers.abstract_dynamic import BaseModelSerializer
from apps.holder.models import ImageHolder, VideoHolder


class VideoHolderSerializer(BaseModelSerializer):
    class Meta:
        model = VideoHolder
        fields = ["uuid", "name", "description", "file"]

    name = serializers.CharField(max_length=100, required=False)


class ImageHolderSerializer(BaseModelSerializer):
    class Meta:
        model = ImageHolder
        fields = ["uuid", "name", "description", "file"]

    name = serializers.CharField(max_length=100, required=False)
