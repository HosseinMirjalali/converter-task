import datetime
import os
import shutil
import subprocess
import uuid
from datetime import timedelta

import ffmpeg
from django.conf import settings

from converter.video.models import VideoConverted, VideoRaw


def convert(raw_uuid: uuid, conv_uuid: uuid) -> VideoConverted:
    """
    A simple converter function that uses ffmpeg wrapper package to execute ffmpeg commands.
    First extracts the given objects' (see params) information from database,
    then makes an output filename that is unique (VideoConverted object's uuid),
    then feeds the file to the ffmpeg input functions, then converts the video
    according to its destination format with proper codecs
    :param raw_uuid: uuid of the VideoRaw object created in view (as passed by the task)
    :param conv_uuid: uuid of the VideoConverted object created in view (as passed by the task)
    :return: conv_obj of VideoConverted type
    """

    raw_obj = VideoRaw.objects.get(uuid=raw_uuid)
    conv_obj = VideoConverted.objects.get(uuid=conv_uuid)
    req_format = raw_obj.req_format
    output_filename = f"{conv_uuid}.{req_format}"
    stream = ffmpeg.input(raw_obj.file.path)
    if req_format == "3gp":
        stream = ffmpeg.output(
            stream, output_filename, vcodec="h263", acodec="aac", s="704x576"
        )
    elif req_format == "mkv":
        stream = ffmpeg.output(stream, output_filename, vcodec="libvpx")
    elif req_format == "avi":
        stream = ffmpeg.output(stream, output_filename, vcodec="mpeg4")
    elif req_format == "mp4":
        stream = ffmpeg.output(stream, output_filename, vcodec="libx264")
    ffmpeg.run(stream)
    # copy the new file to media inside "converted_videos" directory, and then delete the file (here, the conversion
    # process has finished and the raw file is not needed anymore.)
    shutil.copy2(
        output_filename, f"{settings.MEDIA_ROOT}/converted_videos/{output_filename}"
    )
    os.remove(raw_obj.file.path)
    os.remove(output_filename)
    conv_obj.file = f"converted_videos/{output_filename}"
    two_days = datetime.datetime.now() + timedelta(days=2)
    conv_obj.expiration_time = two_days
    conv_obj.save()
    return conv_obj


def get_length(filename: str) -> float:
    """
    using ffprobe, gets the given file's duration in seconds
    :param filename: given by task
    :return: return the result in float
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout)
