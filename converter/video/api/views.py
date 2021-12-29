import datetime
from datetime import timezone
from typing import Any

from dateutil import parser
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from converter.utils.my_converter import get_length
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
            video_length = (
                get_length(serializer.validated_data["file"].temporary_file_path()) / 60
            )
            if (
                request.user.convert_min_left < video_length
            ):  # checks if user has enough conversion charge
                return Response(
                    data="Video length exceeds your remaining charge.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.validated_data["user"] = request.user
            obj = serializer.save()
            conv = VideoConverted.objects.create(user=request.user, raw=obj)
            convert_video_task.apply_async(
                args=(obj.uuid, conv.uuid, request.user.username),
                countdown=1
                # countdown is necessary as the task is async but the database transaction is not
            )
            conv_link = request.build_absolute_uri(
                reverse("videos:download", kwargs={"uuid": conv.uuid})
            )
            response = (
                "Please be patient while we convert the video to your requested format."
                f" Visit {conv_link} and wait until your file is ready for download."
            )
            return Response(data=response, status=status.HTTP_201_CREATED)
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
        try:
            remaining_expiration_time = parser.parse(
                data["expiration_time"]
            ) - datetime.datetime.now(timezone.utc)
            data["remaining_expiration_time"] = remaining_expiration_time
        except TypeError:
            pass
        return Response(data)
