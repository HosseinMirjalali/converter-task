# Generated by Django 3.2.10 on 2021-12-27 11:26

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoRaw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='raw_videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv', '3gp'])])),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_videos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoConverted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='converted_videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv', '3gp'])])),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiration_time', models.DateTimeField(default=datetime.datetime(2021, 12, 29, 14, 56, 47, 846753))),
                ('remaining_expiration_time', models.DateTimeField(blank=True, null=True)),
                ('raw', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='raw', to='video.videoraw')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='converted_videos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
