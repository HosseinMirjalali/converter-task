import datetime
from datetime import timezone
from typing import Any

from dateutil import parser
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from converter.video.api.serializer import VideoConvertedSerializer, VideoRawSerializer
from converter.video.models import VideoConverted, VideoRaw
from converter.video.tasks import convert_video_task


class VideoRawCreateAPIView(CreateAPIView):
    queryset = VideoRaw.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = VideoRawSerializer
    lookup_field = "uuid"

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = VideoRawSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data["user"] = request.user
            obj = serializer.save()
            conv = VideoConverted.objects.create(user=request.user, raw=obj)
            convert_video_task(obj.uuid, conv.uuid)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoConvertedRetrieveAPIView(RetrieveAPIView):
    queryset = VideoConverted.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = VideoConvertedSerializer
    lookup_field = "uuid"

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        remaining_expiration_time = parser.parse(
            data["expiration_time"]
        ) - datetime.datetime.now(timezone.utc)
        data["remaining_expiration_time"] = remaining_expiration_time
        return Response(data)
