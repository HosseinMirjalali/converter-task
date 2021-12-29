import uuid

from celery import shared_task
from django.contrib.auth import get_user_model

from converter.utils.my_converter import convert, get_length
from converter.video.models import VideoConverted

User = get_user_model()


@shared_task
def convert_video_task(raw_uuid: uuid, conv_uuid: uuid, username: str):
    convert(raw_uuid, conv_uuid)  # run the conversion
    user = User.objects.get(username=username)
    video_length = get_length(
        VideoConverted.objects.get(uuid=conv_uuid).file.path
    )  # get user's video length
    video_length /= 60  # divide by 60 for seconds
    user.convert_min_left -= video_length  # deduct from user's total remaining charge
    user.save()
    pass
