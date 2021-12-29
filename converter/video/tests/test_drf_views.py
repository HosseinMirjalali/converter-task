import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from converter.video.api.views import (
    VideoConvertedRetrieveAPIView,
    VideoRawCreateAPIView,
)
from converter.video.models import VideoConverted

User = get_user_model()

UPLOAD_URL = reverse("videos:upload")


class TestUploadVideoView(APITestCase):
    """
    Tests regarding the upload process through the API view
    """

    def setUp(self) -> None:
        """
        Setup for tests
        :return: None
        """
        settings.MEDIA_ROOT = tempfile.mkdtemp()
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create(username="test", password="test")
        self.user.is_active = True
        self.user.save()

    def test_upload_video_unauthenticated(self):
        """
        Endpoint should not be accessible without authentication
        :return:
        """
        view = VideoRawCreateAPIView.as_view()
        request = self.factory.post(UPLOAD_URL)
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_video_upload_authenticated(self):
        """
        Test user can upload a file
        :return:
        """
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        filename = "vid.3gp"
        file = File(open(f"{settings.APPS_DIR}/test_video_files/sample-3gp.3gp", "rb"))
        uploaded_file = SimpleUploadedFile(
            filename, file.read(), content_type="multipart/form-data"
        )
        VideoRawCreateAPIView.as_view()
        data = {"file": uploaded_file, "req_format": "avi"}
        response = self.client.post(UPLOAD_URL, data, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VideoConverted.objects.all().count(), 1)

    def test_user_no_charge_left(self):
        """
        Test user cannot post when they have no charge left
        :return:
        """
        self.user.convert_min_left = 2.05  # the test file is 2 minutes, 6 seconds long
        self.user.save()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        filename = "vid.3gp"
        file = File(open(f"{settings.APPS_DIR}/test_video_files/sample-3gp.3gp", "rb"))
        uploaded_file = SimpleUploadedFile(
            filename, file.read(), content_type="multipart/form-data"
        )
        VideoRawCreateAPIView.as_view()
        data = {"file": uploaded_file, "req_format": "avi"}
        response = self.client.post(UPLOAD_URL, data, format="multipart")
        self.assertEqual(response.status_code, 400)


class TestVideoConvertedAPIView(APITestCase):
    """
    Tests regarding the converted detail video process through the API view
    """

    def setUp(self) -> None:
        """
        Setup for tests
        :return: None
        """
        settings.MEDIA_ROOT = tempfile.mkdtemp()
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create(username="test", password="test")
        self.user.is_active = True
        self.user.save()

    def test_upload_video_unauthenticated(self):
        """
        Endpoint should not be accessible without authentication
        :return:
        """
        view = VideoConvertedRetrieveAPIView.as_view()
        request = self.factory.post(UPLOAD_URL)
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_object_accessible(self):
        """
        Test an existing object is accessible via API
        :return:
        """
        conv_obj = VideoConverted.objects.create(user=self.user, file="test.mp4")
        url = reverse("videos:download", kwargs={"uuid": conv_obj.uuid})
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_object_not_exists(self):
        """
        Test a non-existing object request returns 404
        :return:
        """
        random_uuid = "d043ed9c-b31a-4382-a101-a8bc5b2c57b4"
        VideoConverted.objects.create(user=self.user, file="test.mp4")
        url = reverse("videos:download", kwargs={"uuid": random_uuid})
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
