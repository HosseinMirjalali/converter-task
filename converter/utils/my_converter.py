import ffmpeg

from converter.video.models import VideoRaw, VideoConverted


def convert(raw_uuid, conv_uuid):
    raw_obj = VideoRaw.objects.get(uuid=raw_uuid)
    conv_obj = VideoConverted.objects.get(uuid=conv_uuid)
    req_format = raw_obj.req_format
    output_filename = f"{raw_obj.filename[:-4]}.{req_format}"
    stream = ffmpeg.input(raw_obj.file.path)
    if req_format == "3gp":
        stream = ffmpeg.output(
            stream,
            f"{raw_obj.filename[:-4]}.{req_format}",
            vcodec="h263",
            acodec="aac",
            s="704x576"
        )
    elif req_format == "mkv":
        stream = ffmpeg.output(
            stream,
            output_filename,
            vcodec="libvpx"
        )
    elif req_format == "avi":
        stream = ffmpeg.output(
            stream,
            output_filename,
            vcodec="mpeg4"
        )
    elif req_format == "mp4":
        stream = ffmpeg.output(
            stream,
            output_filename,
            vcodec="mpeg4"
        )
    print(ffmpeg.run(stream))
    conv_obj.file = output_filename
