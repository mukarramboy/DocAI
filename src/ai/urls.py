from celery.app import app_or_default
from django.urls import path

from .views import UploadDocument1View, ChatView

app_name = "ai"

urlpatterns = [
    path("upload/", UploadDocument1View.as_view(), name="upload-document"),
    path("chat/", ChatView.as_view(), name="chat"),
]
