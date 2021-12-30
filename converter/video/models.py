import uuid as uuid_lib

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class VideoRaw(models.Model):
    """
    This model represents the structure for the video the user uploads for conversion
    """

    # possible formats that we can convert, with extra information
    REQUESTED_FORMAT_CHOICES = [
        ("mp4", "mp4, using libx264 codec"),
        ("avi", "avi, using mpeg4 codec"),
        ("mkv", "mkv, using libvpx codec"),
        ("3gp", "3gp, using h263 codec"),
    ]
    user = models.ForeignKey(User, related_name="raw_videos", on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="raw_videos/",
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "avi", "mkv", "3gp"])
        ],
    )
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    req_format = models.CharField(
        _("The format this video should be converted to."),
        max_length=3,
        choices=REQUESTED_FORMAT_CHOICES,
        default="mp4",
    )

    def __str__(self):
        return "%s" % self.uuid


class VideoConverted(models.Model):
    user = models.ForeignKey(
        User, related_name="converted_videos", on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to="converted_videos/",
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "avi", "mkv", "3gp"])
        ],
        blank=True,
    )
    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        editable=False,
        db_index=True,
    )
    raw = models.ForeignKey(
        VideoRaw, related_name="raw", on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(default=None, blank=True, null=True)
    remaining_expiration_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.uuid
