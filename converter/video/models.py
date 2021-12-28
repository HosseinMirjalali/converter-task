import datetime
import os.path
import uuid as uuid_lib
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class VideoRaw(models.Model):
    REQUESTED_FORMAT_CHOICES = [
        ('mp4', 'MPEG-4 Part 14'),
        ('avi', 'AVI'),
        ('mkv', 'Matroska'),
        ('3gp', 'MPEG-4 Part 12')
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
        default='mp4'
    )

    def __str__(self):
        return "%s" % self.uuid

    @property
    def filename(self):
        return os.path.basename(self.file.name)


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
    expiration_time = models.DateTimeField(
        default=None,
        blank=True,
        null=True
    )
    remaining_expiration_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.uuid
