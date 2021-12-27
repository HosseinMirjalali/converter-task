import datetime
import uuid as uuid_lib
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

User = get_user_model()


class VideoRaw(models.Model):
    user = models.ForeignKey(User, related_name="raw_videos", on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="raw_videos/",
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "avi", "mkv", "3gp"])
        ],
    )
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)

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
    expiration_time = models.DateTimeField(
        default=datetime.datetime.now() + timedelta(hours=48)
    )
    remaining_expiration_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.uuid
