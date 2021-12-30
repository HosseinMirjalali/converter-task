import os
import tempfile

import ffmpeg
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from converter.utils.my_converter import convert
from converter.video.models import VideoConverted, VideoRaw

User = get_user_model()

UPLOAD_URL = reverse("videos:upload")


def fileUploader(filename, test_file):
    file = File(open(f"{settings.APPS_DIR}/test_video_files/{test_file}", "rb"))
    uploaded_file = SimpleUploadedFile(
        filename, file.read(), content_type="multipart/form-data"
    )
    return uploaded_file


class TestUploadVideoView(TestCase):
    """
    Tests regarding the upload process through the API view
    """

    def setUp(self) -> None:
        """
        Setup for tests
        :return: None
        """
        settings.MEDIA_ROOT = tempfile.mkdtemp()
        self.conv_dir = os.path.join(settings.MEDIA_ROOT, "converted_videos")
        os.makedirs(self.conv_dir)
        self.filename = "vid.3gp"
        self.file = File(
            open(f"{settings.APPS_DIR}/test_video_files/sample-3gp.3gp", "rb")
        )
        self.uploaded_file = SimpleUploadedFile(
            self.filename, self.file.read(), content_type="multipart/form-data"
        )
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create(username="test", password="test")
        self.user.is_active = True
        self.user.save()
        self.raw_obj_general = VideoRaw.objects.create(
            user=self.user, file=self.uploaded_file, req_format="avi"
        )
        self.raw_obj_general.save()
        self.conv_obj_general = VideoConverted.objects.create(
            user=self.user, file=None, raw=self.raw_obj_general
        )
        self.conv_obj_general.save()

    @pytest.mark.conversion
    def test_convert_general(self):
        """
        A general test with any video file converted to any format
        :return:
        """
        conversion = convert(self.raw_obj_general.uuid, self.conv_obj_general.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "mpeg4")

    # Series of tests that run all the possible conversions, from all 4 formats to all 4 formats (16 cases)
    @pytest.mark.conversion
    def test_convert_mp4_to_mp4(self):
        uploaded_file = fileUploader("vid.mp4", "sample-mp4.mp4")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="mp4"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "h264")

    @pytest.mark.conversion
    def test_convert_mp4_to_avi(self):
        uploaded_file = fileUploader("vid.mp4", "sample-mp4.mp4")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="avi"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "mpeg4")

    @pytest.mark.conversion
    def test_convert_mp4_to_mkv(self):
        uploaded_file = fileUploader("vid.mp4", "sample-mp4.mp4")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="mkv"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "vp8")

    @pytest.mark.conversion
    def test_convert_mp4_to_3gp(self):
        uploaded_file = fileUploader("vid.mp4", "sample-mp4.mp4")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="3gp"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "h263")

    @pytest.mark.conversion
    def test_convert_avi_to_mp4(self):
        uploaded_file = fileUploader("vid.avi", "sample-avi.avi")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="mp4"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "h264")

    @pytest.mark.conversion
    def test_convert_avi_to_avi(self):
        uploaded_file = fileUploader("vid.avi", "sample-avi.avi")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="avi"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "mpeg4")

    @pytest.mark.conversion
    def test_convert_avi_to_mkv(self):
        uploaded_file = fileUploader("vid.avi", "sample-avi.avi")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="mkv"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "vp8")

    @pytest.mark.conversion
    def test_convert_avi_to_3gp(self):
        uploaded_file = fileUploader("vid.avi", "sample-avi.avi")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="3gp"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "h263")

    @pytest.mark.conversion
    def test_convert_mkv_to_mp4(self):
        uploaded_file = fileUploader("vid.mkv", "sample-mkv.mkv")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="mp4"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "h264")

    @pytest.mark.conversion
    def test_convert_mkv_to_avi(self):
        uploaded_file = fileUploader("vid.mkv", "sample-mkv.mkv")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="avi"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "mpeg4")

    @pytest.mark.conversion
    def test_convert_mkv_to_mkv(self):
        uploaded_file = fileUploader("vid.mkv", "sample-mkv.mkv")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="mkv"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "vp8")

    @pytest.mark.conversion
    def test_convert_mkv_to_3gp(self):
        uploaded_file = fileUploader("vid.mkv", "sample-mkv.mkv")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="3gp"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "h263")

    @pytest.mark.conversion
    def test_convert_3gp_to_mp4(self):
        uploaded_file = fileUploader("vid.3gp", "sample-3gp.3gp")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="mp4"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "h264")

    @pytest.mark.conversion
    def test_convert_3gp_to_avi(self):
        uploaded_file = fileUploader("vid.3gp", "sample-3gp.3gp")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="avi"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "mpeg4")

    @pytest.mark.conversion
    def test_convert_3gp_to_mkv(self):
        uploaded_file = fileUploader("vid.3gp", "sample-3gp.3gp")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="mkv"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "vp8")

    @pytest.mark.conversion
    def test_convert_3gp_to_3gp(self):
        uploaded_file = fileUploader("vid.3gp", "sample-3gp.3gp")
        raw_obj_mp4 = VideoRaw.objects.create(
            user=self.user, file=uploaded_file, req_format="3gp"
        )
        raw_obj_mp4.save()
        conv_obj_mp4 = VideoConverted.objects.create(
            user=self.user, file=None, raw=raw_obj_mp4
        )
        conv_obj_mp4.save()
        conversion = convert(raw_obj_mp4.uuid, conv_obj_mp4.uuid)
        stream = ffmpeg.probe(conversion.file.path, v="quiet")
        self.assertEqual(stream["streams"][0]["codec_type"], "video")
        self.assertEqual(stream["streams"][0]["codec_name"], "h263")
