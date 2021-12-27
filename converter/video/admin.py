from django.contrib import admin

from converter.video.models import VideoConverted, VideoRaw


class VideoRawAdmin(admin.ModelAdmin):
    pass


class VideoConvertedAdmin(admin.ModelAdmin):
    pass


admin.site.register(VideoConverted, VideoConvertedAdmin)
admin.site.register(VideoRaw, VideoRawAdmin)
