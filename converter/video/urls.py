from django.urls import path

from converter.video.api import views

app_name = "videos"
urlpatterns = [
    path(route="api/upload", view=views.VideoRawCreateAPIView.as_view(), name="upload"),
    path(
        route="api/video/<uuid:uuid>/",
        view=views.VideoConvertedRetrieveAPIView.as_view(),
        name="download",
    ),
]
