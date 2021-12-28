from celery import shared_task

from converter.utils.my_converter import convert


@shared_task
def convert_video_task(raw_uuid, conv_uuid):
    convert(raw_uuid, conv_uuid)
    pass
