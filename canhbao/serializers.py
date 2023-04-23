from rest_framework import serializers

from canhbao.models.models import Camera


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("id_cam", "name_cam", "port", "name_location")
