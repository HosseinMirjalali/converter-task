from celery import shared_task
from django.contrib.auth import get_user_model

from converter.utils.my_converter import convert, get_length
from converter.video.models import VideoConverted

User = get_user_model()


@shared_task
def convert_video_task(raw_uuid, conv_uuid, username):
    convert(raw_uuid, conv_uuid)
    user = User.objects.get(username=username)
    video_length = get_length(VideoConverted.objects.get(uuid=conv_uuid).file.path)

    user.convert_min_left -= video_length
    user.save()
    pass
