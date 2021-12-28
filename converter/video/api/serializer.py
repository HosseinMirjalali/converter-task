from rest_framework import serializers

from converter.video.models import VideoConverted, VideoRaw


class VideoConvertedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoConverted
        fields = ["user", "file", "uuid", "created_at", "expiration_time"]
        read_only_fields = ["uuid", "user", "created_at", "expiration_time"]
        extra_kwargs = {
            "url": {"view_name": "videos:detail", "lookup_field": "uuid"},
        }


class VideoRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoRaw
        fields = ["user", "file", "uuid", "req_format"]
        read_only_fields = ["uuid", "user"]
